from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
import os

client = AsyncIOMotorClient(
    f"mongodb://{os.getenv("MONGO_HOST")}:{os.getenv("MONGO_PORT")}"
)
db = client[os.getenv("MONGO_DB")]


