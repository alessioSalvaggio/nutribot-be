# app/core/mongo_core.py
import os
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import PyMongoError
from asyncio import Lock

class MongoCore:
    _instance = None
    _lock = Lock()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MongoCore, cls).__new__(cls)
            cls._instance.client = None
            cls._instance.db = None
        return cls._instance

    async def _connect(self):
        if self.client is None:  # Lazy initialization
            async with self._lock:
                if self.client is None:  # Double-check for thread safety
                    try:
                        mongo_host = os.getenv("MONGO_HOST")
                        mongo_port = os.getenv("MONGO_PORT")
                        mongo_db = os.getenv("MONGO_DB")

                        if not all([mongo_host, mongo_port, mongo_db]):
                            raise ValueError("MongoDB environment variables are not set.")

                        mongo_uri = f"mongodb://{mongo_host}:{mongo_port}"
                        self.client = AsyncIOMotorClient(mongo_uri)
                        self.db = self.client[mongo_db]

                    except (ValueError, PyMongoError) as e:
                        print(f"MongoDB connection error: {e}")

    async def get_database(self):
        if self.client is None:
            await self._connect()
        return self.db
    
async def mongo_find_one(collection, query):
    try:
        mongo = MongoCore()
        db = await mongo.get_database()
        result = await db[collection].find_one(query)
        return result
    except PyMongoError as e:
        print(f"Error finding one document in {collection}: {e}")

async def mongo_insert_one(collection, document):
    try:
        mongo = MongoCore()
        db = await mongo.get_database()
        result = await db[collection].insert_one(document)
        return result
    except PyMongoError as e:
        print(f"Error inserting one document into {collection}: {e}")

async def mongo_update_one(collection, query, update):
    try:
        mongo = MongoCore()
        db = await mongo.get_database()
        result = await db[collection].update_one(query, update)
        return result
    except PyMongoError as e:
        print(f"Error updating one document in {collection}: {e}")

async def mongo_find_many(collection, query):
    try:
        mongo = MongoCore()
        db = await mongo.get_database()
        cursor = db[collection].find(query)
        return cursor
    except PyMongoError as e:
        print(f"Error finding many documents in {collection}: {e}")
        
async def mongo_delete_many(collection, query):
    try:
        mongo = MongoCore()
        db = await mongo.get_database()
        return await db[collection].delete_many(query)
    except PyMongoError as e:
        print(f"Error deleting many documents in {collection}: {e}")