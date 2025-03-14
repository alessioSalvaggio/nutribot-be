from fastapi import APIRouter, HTTPException, Request
from app.core.mongo_core import mongo_insert_one, mongo_find_one, mongo_find_many, mongo_update_one
from app.models import NewPatientProfile, NewMeasRequest
from app.core.communication_utils import send_multi_email
from app.utils.connector_3d_look import generate_new_measurement_widget
from app.core.mongo_logging import log_to_mongo
import os
from bson import ObjectId
import json
from datetime import datetime

RETURN_HOME_URL_3DLOOK_WIDGET = os.getenv("RETURN_HOME_URL_3DLOOK_WIDGET")
with open(os.getenv("LOOK3D_MEASUREMENTS_STRUCTURE"), "r") as f:
    structure_3dl_measurements = json.load(f)

router = APIRouter()

@router.post("/add_new_patient")
async def save_item(patient_profile: NewPatientProfile, request: Request):
    try:
        patient_profile = patient_profile.model_dump()
        patient_profile['misurazioni'] = {}
        patient_profile['nutrizionista'] = request.state.user_id
        result = await mongo_insert_one("patients", patient_profile)
        if result.inserted_id:
            await log_to_mongo(request.state.user_id, "app/api/endpoints/manage_patients/save_item", "INFO", f"New patient {result.inserted_id} added by nutrizionista {request.state.user_id}")
            return {"message": "Item saved successfully", "id": str(result.inserted_id)}
        else:
            await log_to_mongo(request.state.user_id, "app/api/endpoints/manage_patients/save_item", "ERROR", f"Failed to save new patient by nutrizionista {request.state.user_id}")
            raise HTTPException(status_code=500, detail="Failed to save item")
    except Exception as e:
        await log_to_mongo(request.state.user_id, "app/api/endpoints/manage_patients/save_item", "ERROR", f"Exception occurred while saving new patient by nutrizionista {request.state.user_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to save item")

@router.get("/all_patients")
async def get_patients(request: Request):
    try:
        nutrizionista_id = request.state.user_id
        patients_cursor = await mongo_find_many("patients", {"nutrizionista": nutrizionista_id})
        patients = await patients_cursor.to_list(length=None)
        for p in patients:
            p['_id'] = str(p['_id'])
            if not 'misurazioni' in p:
                await mongo_update_one("patients", {"_id": ObjectId(p['_id'])}, {"$set": {"misurazioni": {}}})
        for p in patients:
            if 'misurazioni' in p:
                del p['misurazioni']
                
        return patients
    except Exception as e:
        await log_to_mongo(request.state.user_id, "app/api/endpoints/manage_patients/get_patients", "ERROR", f"Failed to retrieve patients for nutrizionista {nutrizionista_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve patients")

@router.post("/request_new_measurement")
async def request_new_measurement(new_measurement_request: NewMeasRequest, request: Request):
    try:
        patient_details = await mongo_find_one("patients", {"_id": ObjectId(new_measurement_request.patId)})
        if sum([v=={} for k,v in patient_details['misurazioni'].items()]) > 0:
            await log_to_mongo(request.state.user_id, "app/api/endpoints/manage_patients/request_new_measurement", "WARNING", f"Measurement already pending for patient {new_measurement_request.patId}")
            return "measurement already pending"
        
        pat_email = patient_details['email']
        pat_first_name = patient_details['nome'] + " " + patient_details['cognome'] 
        pat_gender_tag = "GENDER_PAGE_MALE_GENDER_SELECTED" if patient_details['genere'].lower() == "maschio" else "GENDER_PAGE_FEMALE_GENDER_SELECTED"
        pat_gender = "male" if patient_details['genere'].lower() == "maschio" else "female"
        pat_height = patient_details['altezza']
        pat_weight = patient_details['peso']
        return_url = RETURN_HOME_URL_3DLOOK_WIDGET
        
        result, UUID = generate_new_measurement_widget(pat_email, pat_first_name, pat_gender_tag, pat_gender, pat_height, pat_weight, return_url)
        await mongo_update_one("patients", {"_id": ObjectId(new_measurement_request.patId)},{"$set": {f"misurazioni.{UUID}": {}}})
        await mongo_insert_one("measurements", {
                "UUID": UUID, 
                "requestedOn": datetime.now(), 
                "patientId": new_measurement_request.patId, 
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
        await log_to_mongo(request.state.user_id, "app/api/endpoints/manage_patients/request_new_measurement", "INFO", f"New measurement requested for patient {new_measurement_request.patId}")
        return "success"
    except Exception as e:
        await log_to_mongo(request.state.user_id, "app/api/endpoints/manage_patients/request_new_measurement", "ERROR", f"Failed to request new measurement for patient {new_measurement_request.patId}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to request new measurement")

@router.get("/get_patient_measurements")
async def get_patient_measurements(patientId: str, request: Request):
    try:
        patient_details = await mongo_find_one('patients', {"_id": ObjectId(patientId)})
        if not patient_details:
            await log_to_mongo(request.state.user_id, "app/api/endpoints/manage_patients/get_patient_measurements", "ERROR", f"Patient {patientId} not found")
            raise HTTPException(status_code=404, detail="Patient not found")
        
        measurements = []
        for uuid, measurement in patient_details.get('misurazioni', {}).items():
            if measurement == {}:
                measurements.append(
                    {
                        "UUID": uuid,
                        "completed": False
                    }
                )
            else:
                measurements.append(
                    {
                        "UUID": uuid,
                        "data": datetime.strptime(measurement.get('data', None), "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%d/%m/%Y") if measurement.get('data', None) else None,
                        "valori": [
                            {
                                "misura": structure_3dl_measurements[k]['it_name'], 
                                "valore": v
                            } for k, v in measurement.get('valori', {}).items()
                        ],
                        "completed": True
                    }
                )
        await log_to_mongo(request.state.user_id, "app/api/endpoints/manage_patients/get_patient_measurements", "INFO", f"Retrieved measurements for patient {patientId}")
        return measurements
    except Exception as e:
        await log_to_mongo(request.state.user_id, "app/api/endpoints/manage_patients/get_patient_measurements", "ERROR", f"Failed to retrieve measurements for patient {patientId}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve measurements")