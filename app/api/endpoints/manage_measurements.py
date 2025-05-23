from fastapi import APIRouter, HTTPException, Request
from hypaz_core.mongo_core import mongo_find_one
from hypaz_core.mongo_logging import log_to_mongo
from app.core.data_accessibility import has_access_to_measure

router = APIRouter()

@router.get("/{measureUUId}")
async def get_single_measurement(measureUUId: str, request: Request):
    try:
        if not await has_access_to_measure(request.state.user_id, measureUUId):
            raise HTTPException(status_code=403, detail=f"Access denied for User {request.state.user_id} to Measurement {measureUUId}")
        
        measurement_details = await mongo_find_one("measurements", {"UUID": measureUUId})
        if "gender" in measurement_details["result"]["state"]:
            gender = measurement_details["result"]["state"]["gender"]
            height = measurement_details["result"]["state"]["height"]
            weight = measurement_details["result"]["state"]["weight"]
        else:
            gender = measurement_details["result"]["state"]["measurements"]["gender"]
            height = measurement_details["result"]["state"]["measurements"]["height"]
            weight = measurement_details["result"]["state"]["measurements"]["weight"]
        if not measurement_details:
            await log_to_mongo(request.state.user_id, "app/api/endpoints/manage_measurements/get_single_measurement", "ERROR", f"Measurement {measureUUId} not found")
            raise HTTPException(status_code=404, detail="Measurement not found")
        measurement_details_result = {
            "_id": str(measurement_details['_id']),
            "UUID": measurement_details["UUID"],
            "patientId": measurement_details["patientId"],
            "nutrizionista": measurement_details["nutrizionista"],
            "gender": gender,
            "height": height,
            "weight": weight,
            "date": measurement_details["result"]["updated"],
            "volume_params": measurement_details["result"]["state"]["measurements"]["volume_params"]
        }
        return measurement_details_result
    except Exception as e:
        await log_to_mongo(request.state.user_id, "app/api/endpoints/manage_measurements/get_single_measurement", "ERROR", f"Failed to retrieve measurement {measureUUId}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve measurement")
    