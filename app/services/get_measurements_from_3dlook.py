import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from dotenv import load_dotenv 
load_dotenv(dotenv_path="/home/alessio/nutribot/.env")

from hypaz_core.mongo_core import mongo_find_many, mongo_update_one
from hypaz_core.mongo_logging import log_to_mongo 
import asyncio
from app.utils.connector_3d_look import get_measurement_widget_data
from bson import ObjectId

async def check_and_get_pending_measures():
    try:
        measurements_cursor = await mongo_find_many("measurements", {"result": {"$exists": False}})
        measurements = await measurements_cursor.to_list(length=None)
        completed_measurements = {}
        pending_measurements = {}
        for m in measurements:
            result = get_measurement_widget_data(m['UUID'])
            try:
                result['uuid']
            except:
                await log_to_mongo(
                    "3DLOOK_GET_MEASUREMENTS_JOB", 
                    "app/services/get_measurements_from_3dlook/check_and_get_pending_measures", 
                    "WARNING", 
                    f"Measurement {m['UUID']} for patient {m["patientId"]} NOT found in 3DLOOK"
                )
            
            if 'status' in result['state'] and result['state']['status'] == 'finished':
                completed_measurements[m["UUID"]] = {"patient": m["patientId"]}
                await mongo_update_one("measurements", {"_id": m["_id"]},{"$set": {"result": result}})
                await mongo_update_one('patients', {"_id": ObjectId(m["patientId"])},
                    {
                        "$set": {
                            f"misurazioni.{m['UUID']}": {
                                'data':result['updated'],
                                'valori':result['state']['measurements']['volume_params']
                            }
                        }
                    })
            else:
                pending_measurements[m["UUID"]] = {"patient": m["patientId"]}
        
        if len(completed_measurements) > 0:
            log_content = {
                f"{len(completed_measurements)} COMPLETED MEASUREMENTS": completed_measurements,
                f"{len(pending_measurements)} PENDING MEASUREMENTS": pending_measurements
            }
            await log_to_mongo(
                "3DLOOK_GET_MEASUREMENTS_JOB", 
                "app/services/get_measurements_from_3dlook/check_and_get_pending_measures", 
                "INFO", 
                f"{log_content}"
            )
    except Exception as e:
        await log_to_mongo(
            "3DLOOK_GET_MEASUREMENTS_JOB", 
            "app/services/get_measurements_from_3dlook/check_and_get_pending_measures", 
            "ERROR", 
            f"{str(e)}"
        )     
       
if __name__ == "__main__":
    asyncio.run(check_and_get_pending_measures())