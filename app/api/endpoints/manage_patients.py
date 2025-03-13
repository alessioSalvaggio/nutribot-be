from fastapi import APIRouter, HTTPException, Request
from app.core.mongo_core import db
from app.models import NewPatientProfile, NewMeasRequest
from app.core.communication_utils import send_multi_email
from app.utils.connector_3d_look import generate_new_measurement_widget
import os
from bson import ObjectId
from datetime import datetime

RETURN_HOME_URL_3DLOOK_WIDGET = os.getenv("RETURN_HOME_URL_3DLOOK_WIDGET")

router = APIRouter()

@router.post("/add_new_patient")
async def save_item(patient_profile: NewPatientProfile, request: Request):
    patient_profile = patient_profile.model_dump()
    patient_profile['misurazioni'] = {}
    patient_profile['nutrizionista'] = request.state.user_id
    result = await db["patients"].insert_one(patient_profile)
    if result.inserted_id:
        return {"message": "Item saved successfully", "id": str(result.inserted_id)}
    else:
        raise HTTPException(status_code=500, detail="Failed to save item")

@router.get("/all_patients")
async def get_patients(request: Request):
    nutrizionista_id = request.state.user_id
    patients = await db["patients"].find({"nutrizionista": nutrizionista_id}).to_list(length=None)
    for p in patients:
        p['_id'] = str(p['_id'])
        if not 'misurazioni' in p:
            result = await db["patients"].update_one(
                {"_id": ObjectId(p['_id'])},
                {"$set": {f"misurazioni": {}}}
            )
    for p in patients:
        if 'misurazioni' in p:
            del p['misurazioni']
            
    return patients

@router.post("/request_new_measurement")
async def request_new_measurement(new_measurement_request: NewMeasRequest, request: Request):
    patient_details = await db['patients'].find_one({"_id": ObjectId(new_measurement_request.patId)})
    if sum([v=={} for k,v in patient_details['misurazioni'].items()]) > 0:
        return "measurement already pending"
    
    pat_email = patient_details['email']
    pat_first_name = patient_details['nome'] + " " + patient_details['cognome'] 
    pat_gender_tag = "GENDER_PAGE_MALE_GENDER_SELECTED" if patient_details['genere'].lower() == "maschio" else "GENDER_PAGE_FEMALE_GENDER_SELECTED"
    pat_gender = "male" if patient_details['genere'].lower() == "maschio" else "female"
    pat_height = patient_details['altezza']
    pat_weight = patient_details['peso']
    return_url = RETURN_HOME_URL_3DLOOK_WIDGET
    
    # result, UUID = generate_new_measurement_widget(pat_email, pat_first_name, pat_gender_tag, pat_gender, pat_height, pat_weight, return_url)
    # await db["patients"].update_one(
    #     {"_id": ObjectId(new_measurement_request.patId)},
    #     {"$set": {f"misurazioni.{UUID}": {}}}
    # )
    # await db["measurements"].insert_one(
    #     {
    #         "UUID": UUID, 
    #         "requestedOn": datetime.now(), 
    #         "patientId": new_measurement_request.patId, 
    #         "nutrizionista": request.state.user_id
    #     }
    # )
    result = {
        "short_link": "https://hypaz.com"
    }
    
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
    return "success"

@router.get("/get_patient_measurements")
async def get_patient_measurements(patient_id: str):
    patient_details = await db['patients'].find_one({"_id": ObjectId(patient_id)})
    if not patient_details:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    measurements = []
    for uuid, measurement in patient_details.get('misurazioni', {}).items():
        measurement_details = await db['measurements'].find_one({"UUID": uuid})
        if measurement_details:
            measurement_details['_id'] = str(measurement_details['_id'])
            measurements.append(measurement_details)
    
    return measurements