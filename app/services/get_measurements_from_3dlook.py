import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.core.mongo_core import db
from app.core.mongo_logging import log_to_mongo 
import asyncio
from app.utils.connector_3d_look import get_measurement_widget_data
from bson import ObjectId

async def check_and_get_pending_measures():
    measurements = await db["measurements"].find({"result": {"$exists": False}}).to_list(length=None)
    for m in measurements:
        result = get_measurement_widget_data(m['UUID'])
        try:
            result['uuid']
        except:
            await log_to_mongo("app/services/check_measurements_status/read_all_measurements", "WARNING", f"Measurement {m['UUID']} for patient {m["patientId"]} NOT found in 3DLOOK")
        
        if 'status' in result['state'] and result['state']['status'] == 'finished':
            await log_to_mongo(
                "app/services/check_measurements_status/read_all_measurements", 
                "INFO", 
                f"Measurement {m['UUID']} COMPLETED for patient {m["patientId"]}"
            )
            await db["measurements"].update_one(
                {"_id": m["_id"]},
                {"$set": {"result": result}}
            )
            patient_update_result = await db['patients'].update_one(
                {"_id": ObjectId(m["patientId"])},
                {
                    "$set": {
                        f"misurazioni.{m['UUID']}": {
                            'data':result['updated'],
                            'valori':result['state']['measurements']['volume_params']
                        }
                    }
                }
            )
            await log_to_mongo(
                "app/services/check_measurements_status/read_all_measurements", 
                "INFO", 
                f"Data inserted in DB for Measurement {m['UUID']} for patient {m["patientId"]}"
            )
        else:
            await log_to_mongo(
                "app/services/check_measurements_status/read_all_measurements", 
                "INFO", 
                f"Measurement {m['UUID']} NOT COMPLETED for patient {m["patientId"]}"
            )
            
if __name__ == "__main__":
    asyncio.run(check_and_get_pending_measures())