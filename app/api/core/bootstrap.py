import os
import firebase_admin
from firebase_admin import credentials
from app.core.mongo_core import MongoCore

def init_services():
    mongo = MongoCore()

    cred_path = os.getenv("FIREBASE_CREDENTIALS_PATH")
    if not cred_path:
        raise ValueError("FIREBASE_CREDENTIALS_PATH environment variable not set")
    
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)

    return {
        "mongo": mongo,
        "firebase": firebase_admin,
    }