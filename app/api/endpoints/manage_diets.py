from fastapi import APIRouter, HTTPException
from app.utils.diet_utils import make_diet, generate_diet_pdf

router = APIRouter()

@router.post("/make_diet/{patient_id}")
async def make_diet_endpoint(patient_id: str):
    """
    Generate a diet plan for a given patient ID.
    """
    try:
        diet_id = await make_diet(patient_id)
        if not diet_id:
            raise HTTPException(status_code=500, detail="Failed to generate diet plan.")
        return {"message": "Diet plan generated successfully.", "diet_id": str(diet_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/generate_diet_pdf/{diet_id}")
async def generate_diet_pdf_endpoint(diet_id: str):
    """
    Generate a PDF for a given diet ID.
    """
    try:
        await generate_diet_pdf(diet_id)
        return {"message": "Diet PDF generated successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
