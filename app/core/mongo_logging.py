import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import os
from app.core.mongo_core import mongo_insert_one
from datetime import datetime
import pytz
import asyncio

ENV_TYPE = os.getenv("ENV_TYPE")

async def log_to_mongo(user: str, app_function: str, level: str, message: str):
    timestamp = datetime.now(pytz.timezone('Europe/Rome')).strftime('%Y-%m-%dT%H:%M:%S.')
    log_entry = {
        "app": "nutribot",
        "user": user,
        "environment": ENV_TYPE,
        "function": app_function,
        "level": level,
        "ts": timestamp,
        "content": message
    }
    result = await mongo_insert_one("logs", log_entry)
    print(log_entry)
    
if __name__=="__main__":
    asyncio.run(log_to_mongo("DEBUG_MONGO_LOGGING", "app/send_email", "INFO", f"Sending email to someone")) 
