from fastapi import APIRouter, HTTPException, Request
from app.core.database import db
from app.models import NewPatientProfile

router = APIRouter()

@router.post("/add_new_patient")
async def save_item(patient_profile: NewPatientProfile, request: Request):
    patient_profile = patient_profile.model_dump()
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
    return patients