import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.core.mongo_core import mongo_find_many, mongo_update_one
from app.core.mongo_logging import log_to_mongo 
import asyncio
from app.utils.connector_3d_look import get_measurement_widget_data
from bson import ObjectId

async def check_and_get_pending_measures():
    measurements_cursor = await mongo_find_many("measurements", {"result": {"$exists": False}})
    measurements = await measurements_cursor.to_list(length=None)
    for m in measurements:
        result = get_measurement_widget_data(m['UUID'])
        try:
            result['uuid']
        except:
            await log_to_mongo("3DLOOK_GET_MEASUREMENTS_JOB", "app/services/get_measurements_from_3dlook/check_and_get_pending_measures", "WARNING", f"Measurement {m['UUID']} for patient {m["patientId"]} NOT found in 3DLOOK")
        
        if 'status' in result['state'] and result['state']['status'] == 'finished':
            await log_to_mongo(
                "3DLOOK_GET_MEASUREMENTS_JOB", 
                "app/services/get_measurements_from_3dlook/check_and_get_pending_measures", 
                "INFO", 
                f"Measurement {m['UUID']} COMPLETED for patient {m["patientId"]}"
            )
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
            
            await log_to_mongo(
                "3DLOOK_GET_MEASUREMENTS_JOB", 
                "app/services/get_measurements_from_3dlook/check_and_get_pending_measures", 
                "INFO", 
                f"Data inserted in DB for Measurement {m['UUID']} for patient {m["patientId"]}"
            )
        else:
            await log_to_mongo(
                "3DLOOK_GET_MEASUREMENTS_JOB", 
                "app/services/get_measurements_from_3dlook/check_and_get_pending_measures", 
                "INFO", 
                f"Measurement {m['UUID']} NOT COMPLETED for patient {m["patientId"]}"
            )
            
if __name__ == "__main__":
    asyncio.run(check_and_get_pending_measures())