from fastapi import APIRouter, HTTPException, Request
from app.utils.diet_utils import make_diet, generate_diet_pdf, send_diet_email
from app.core.data_accessibility import has_access_to_user, has_access_to_diet

router = APIRouter()

@router.post("/make_diet/{patient_id}")
async def diet_making(patient_id: str, request: Request):
    """
    Generate a diet plan for a given patient ID.
    """
    try:
        if not await has_access_to_user(request.state.user_id, patient_id):
            raise HTTPException(status_code=403, detail=f"Access denied for User {request.state.user_id} to Patient {patient_id}")
        
        diet_id = await make_diet(patient_id, request.state.user_id)
        if not diet_id:
            raise HTTPException(status_code=500, detail="Failed to generate diet plan.")
        return {"message": "Diet plan generated successfully.", "diet_id": str(diet_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/generate_diet_pdf/{diet_id}")
async def diet_pdf_generation(diet_id: str, request: Request):
    """
    Generate a PDF for a given diet ID.
    """
    try:
        if not await has_access_to_diet(request.state.user_id, diet_id):
            raise HTTPException(status_code=403, detail=f"Access denied for User {request.state.user_id} to Diet {diet_id}")

        await generate_diet_pdf(diet_id)
        return {"message": "Diet PDF generated successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/send_diet_email/{diet_id}")
async def diet_sending_email(diet_id: str, request: Request):
    """
    Send the generated diet PDF to the user's email.
    """
    try:
        if not await has_access_to_diet(request.state.user_id, diet_id):
            raise HTTPException(status_code=403, detail=f"Access denied for User {request.state.user_id} to Diet {diet_id}")

        await send_diet_email(diet_id, request.state.email)
        return {"message": "Diet email sent successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))