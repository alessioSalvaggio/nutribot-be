import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from dotenv import load_dotenv 
load_dotenv(dotenv_path="/home/alessio/nutribot/.env")

from datetime import datetime, timedelta
from hypaz_core.mongo_core import mongo_delete_many
from hypaz_core.mongo_logging import log_to_mongo
from app.config.generic_conf import LOG_RETENTION_DAYS

class DBRetentionJob:
    async def apply_retention_policy(self):
        try:
            retention_start_date = datetime.now() - timedelta(days=LOG_RETENTION_DAYS)
            result = await mongo_delete_many('logs',{'timestamp': {'$lt': retention_start_date}})
            await log_to_mongo("DB_RETENTION_JOB", "app/services/db_retention_job/apply_retention_policy", "INFO", f"Deleted {result.deleted_count} documents older than 3 months.")
        except Exception as e:
            await log_to_mongo("DB_RETENTION_JOB", "app/services/db_retention_job/apply_retention_policy", "ERROR", f"An error occurred: {str(e)}")

if __name__ == "__main__":
    import asyncio
    retention_job = DBRetentionJob()
    asyncio.run(retention_job.apply_retention_policy())
