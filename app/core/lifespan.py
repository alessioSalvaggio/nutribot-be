from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.mongo_core import MongoCore

mongo = MongoCore()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await mongo._connect()
    print("Connected to MongoDB.")
    yield
    if mongo.client:
        mongo.client.close()
        print("MongoDB connection closed.")
