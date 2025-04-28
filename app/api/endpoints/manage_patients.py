from fastapi import APIRouter, HTTPException, Request
from app.models import NewPatientProfile
from app.core.communication_utils import send_multi_email
from app.core.mongo_logging import log_to_mongo
from app.core.mongo_core import mongo_insert_one, mongo_find_one, mongo_find_many, mongo_update_one
from app.core.data_accessibility import has_access_to_user
from app.utils.connector_3d_look import generate_new_measurement_widget
import os
from bson import ObjectId
import json
from datetime import datetime, date

RETURN_HOME_URL_3DLOOK_WIDGET = os.getenv("RETURN_HOME_URL_3DLOOK_WIDGET")
with open(os.getenv("LOOK3D_MEASUREMENTS_STRUCTURE"), "r") as f:
    structure_3dl_measurements = json.load(f)

router = APIRouter()

def serialize_document(doc):
    for key, value in doc.items():
        if isinstance(value, dict):
            doc[key] = serialize_document(value)  # Ricorsione per i dizionari annidati
        elif isinstance(value, date):
            doc[key] = value.isoformat()  # Converti la data in stringa
    return doc

@router.post("/add_new")
async def save_item(patient_profile: NewPatientProfile, request: Request):
    try:
        patient_profile = patient_profile.model_dump()
        patient_profile['misurazioni'] = {}
        patient_profile['nutrizionista'] = request.state.user_id

        result = await mongo_insert_one("patients", serialize_document(patient_profile))
        if result.inserted_id:
            await log_to_mongo(request.state.user_id, "app/api/endpoints/manage_patients/save_item", "INFO", f"New patient {result.inserted_id} added by nutrizionista {request.state.user_id}")
            return {"message": "Item saved successfully", "id": str(result.inserted_id)}
        else:
            await log_to_mongo(request.state.user_id, "app/api/endpoints/manage_patients/save_item", "ERROR", f"Failed to save new patient by nutrizionista {request.state.user_id}")
            raise HTTPException(status_code=500, detail="Failed to save item")
    except Exception as e:
        await log_to_mongo(request.state.user_id, "app/api/endpoints/manage_patients/save_item", "ERROR", f"Exception occurred while saving new patient by nutrizionista {request.state.user_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to save item")

@router.get("/")
async def get_patients(request: Request):
    try:
        nutrizionista_id = request.state.user_id
        # Add filter to exclude documents where "deleted" is true
        patients_cursor = await mongo_find_many(
            "patients", 
            {"nutrizionista": nutrizionista_id, "$or": [{"deleted": {"$exists": False}}, {"deleted": False}]}
        )
        patients = await patients_cursor.to_list(length=None)
        patients_result = []
        for p in patients:
            if 'personal_info' in p:
                curr_patient_pers_info = {'_id': str(p['_id'])}
                curr_patient_pers_info.update({k:v for k,v in p['personal_info'].items() if k!='_id'})
                patients_result.append(curr_patient_pers_info)
            else:
                p['_id'] = str(p['_id'])
                patients_result.append(p)
                
        for p in patients_result:
            if 'misurazioni' in p:
                del p['misurazioni']
                
        return patients_result
    except Exception as e:
        await log_to_mongo(request.state.user_id, "app/api/endpoints/manage_patients/get_patients", "ERROR", f"Failed to retrieve patients for nutrizionista {nutrizionista_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve patients")

@router.get("/{patientId}/request_measurement")
async def request_new_measurement(patientId: str, request: Request):
    if not await has_access_to_user(request.state.user_id, patientId):
        raise HTTPException(status_code=403, detail=f"Access denied for User {request.state.user_id} to Patient {patientId}")
    try:
        patient_details = await mongo_find_one("patients", {"_id": ObjectId(patientId)})
        if sum([v=={} for k,v in patient_details['misurazioni'].items()]) > 0:
            await log_to_mongo(request.state.user_id, "app/api/endpoints/manage_patients/request_new_measurement", "WARNING", f"Measurement already pending for patient {patientId}")
            raise HTTPException(status_code=500, detail="Measurement already pending")
        
        pat_email = patient_details['personal_info']['email']
        pat_first_name = patient_details['personal_info']['nome'] + " " + patient_details['personal_info']['cognome'] 
        pat_gender_tag = "GENDER_PAGE_MALE_GENDER_SELECTED" if patient_details['personal_info']['gender'].lower() == "maschio" else "GENDER_PAGE_FEMALE_GENDER_SELECTED"
        pat_gender = "male" if patient_details['personal_info']['gender'].lower() == "maschio" else "female"
        pat_height = patient_details['personal_info']['altezza']
        pat_weight = patient_details['weight_history']['peso_attuale']
        return_url = RETURN_HOME_URL_3DLOOK_WIDGET
        
        result, UUID = generate_new_measurement_widget(pat_email, pat_first_name, pat_gender_tag, pat_gender, pat_height, pat_weight, return_url)
        await mongo_update_one("patients", {"_id": ObjectId(patientId)},{"$set": {f"misurazioni.{UUID}": {}}})
        await mongo_insert_one("measurements", {
                "UUID": UUID, 
                "requestedOn": datetime.now(), 
                "patientId": patientId, 
                "nutrizionista": request.state.user_id
            })
        
        body = (
            f"Ciao {pat_first_name},<br><br>"
            "Il tuo nutrizionista ha richiesto una misurazione per te.<br>"
            "Per favore, clicca sul seguente link per iniziare il processo di misurazione:<br>"
            f"<a href='{result['short_link']}'>{result['short_link']}</a><br><br>"
            "Grazie,<br>"
            "Il team di NutriBot"
        )
        await send_multi_email(
            ['nutribot@hypaz.com', 'scolettasilvia@gmail.com'],
            "Richiesta di misurazione",
            body
        )
        await log_to_mongo(request.state.user_id, "app/api/endpoints/manage_patients/request_new_measurement", "INFO", f"New measurement requested for patient {patientId}")
        return "success"
    except Exception as e:
        await log_to_mongo(request.state.user_id, "app/api/endpoints/manage_patients/request_new_measurement", "ERROR", f"Failed to request new measurement for patient {patientId}: {str(e)}")
        raise e

@router.get("/{patientId}")
async def get_patient_info(patientId: str, request: Request):
    if not await has_access_to_user(request.state.user_id, patientId):
        raise HTTPException(status_code=403, detail=f"Access denied for User {request.state.user_id} to Patient {patientId}")
    try:
        patient_details = await mongo_find_one('patients', {"_id": ObjectId(patientId)})
        if not patient_details:
            await log_to_mongo(request.state.user_id, "app/api/endpoints/manage_patients/get_patient_info", "ERROR", f"Patient {patientId} not found")
            raise HTTPException(status_code=404, detail="Patient not found")
        patient_details['_id'] = str(patient_details['_id'])
        patient_details["misurazioni"] = dict(sorted(patient_details["misurazioni"].items(), key=lambda x: x[1].get("data", "9999-12-31T23:59:59.999999Z"), reverse=True))
        return patient_details
    except Exception as e:
        await log_to_mongo(request.state.user_id, "app/api/endpoints/manage_patients/get_patient_info", "ERROR", f"Failed to retrieve information for patient {patientId}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve patient information")
    
@router.put("/{patientId}")
async def update_patient_info(patientId: str, updated_profile: NewPatientProfile, request: Request):
    if not await has_access_to_user(request.state.user_id, patientId):
        raise HTTPException(status_code=403, detail=f"Access denied for User {request.state.user_id} to Patient {patientId}")
    try:
        updated_data = updated_profile.model_dump()
        result = await mongo_update_one(
            "patients",
            {"_id": ObjectId(patientId)},
            {"$set": serialize_document(updated_data)}
        )
        if result.modified_count == 1:
            return {"message": "Patient updated successfully"}
        else:
            await log_to_mongo(request.state.user_id, "app/api/endpoints/manage_patients/update_patient_info", "ERROR", f"Failed to update patient {patientId} by nutrizionista {request.state.user_id}")
            raise HTTPException(status_code=404, detail="Patient not found or no changes made")
    except Exception as e:
        await log_to_mongo(request.state.user_id, "app/api/endpoints/manage_patients/update_patient_info", "ERROR", f"Exception occurred while updating patient {patientId} by nutrizionista {request.state.user_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update patient")

@router.delete("/{patientId}")
async def delete_patient(patientId: str, request: Request):
    if not await has_access_to_user(request.state.user_id, patientId):
        raise HTTPException(status_code=403, detail=f"Access denied for User {request.state.user_id} to Patient {patientId}")
    try:
        result = await mongo_update_one(
            "patients",
            {"_id": ObjectId(patientId)},
            {"$set": {"deleted": True}}  # Soft delete by marking as deleted
        )
        if result.modified_count == 1:
            return {"message": "Patient deleted successfully"}
        else:
            await log_to_mongo(request.state.user_id, "app/api/endpoints/manage_patients/delete_patient", "ERROR", f"Failed to delete patient {patientId} by nutrizionista {request.state.user_id}")
            raise HTTPException(status_code=404, detail="Patient not found")
    except Exception as e:
        await log_to_mongo(request.state.user_id, "app/api/endpoints/manage_patients/delete_patient", "ERROR", f"Exception occurred while deleting patient {patientId} by nutrizionista {request.state.user_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to delete patient")
    
@router.get("/{patientId}/measurements")
async def get_patient_measurements(patientId: str, request: Request):
    if not await has_access_to_user(request.state.user_id, patientId):
        raise HTTPException(status_code=403, detail=f"Access denied for User {request.state.user_id} to Patient {patientId}")
    try:
        patient_details = await mongo_find_one("patients", {"_id": ObjectId(patientId)})
        if not patient_details:
            await log_to_mongo(request.state.user_id, "app/api/endpoints/manage_patients/get_patient_measurements", "ERROR", f"Patient {patientId} not found")
            raise HTTPException(status_code=404, detail="Patient not found")
        
        if "misurazioni" not in patient_details:
            await log_to_mongo(request.state.user_id, "app/api/endpoints/manage_patients/get_patient_measurements", "ERROR", f"No measurements field in patient {patientId}")
            return {"message": "No measurements field for this patient"}
        
        measurements = patient_details.get("misurazioni", {})
        ordered_measurements = dict(sorted(measurements.items(), key=lambda x: x[1].get("data", "9999-12-31T23:59:59.999999Z"), reverse=True))
        return ordered_measurements
    
    except Exception as e:
        await log_to_mongo(request.state.user_id, "app/api/endpoints/manage_patients/get_patient_measurements", "ERROR", f"Failed to retrieve measurements for patient {patientId}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve measurements")
    
    
    