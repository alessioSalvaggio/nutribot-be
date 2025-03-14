import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.api.endpoints import manage_patients
import firebase_admin
from firebase_admin import auth, credentials
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
        
app = FastAPI(root_path="/nutribot/api")

cred_path = os.getenv("FIREBASE_CREDENTIALS_PATH")
if not cred_path:
    raise ValueError("FIREBASE_CREDENTIALS_PATH environment variable not set")

# Initialize Firebase Admin SDK
cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred)

@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    override_api_auth_token = os.getenv("OVERRIDE_API_AUTH_TOKEN")

    if request.url.path.startswith("/docs") or request.url.path.startswith("/openapi.json"):
        return await call_next(request)
    
    jwt_token = request.headers.get("Authorization")
    if jwt_token:
        if jwt_token == override_api_auth_token:
            request.state.user_id = "override_token_dev_user"
            return await call_next(request)
        else:
            try:
                decoded_token = auth.verify_id_token(jwt_token)
                request.state.user_id = decoded_token["uid"]
            except Exception as e:
                raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    else:
        raise HTTPException(status_code=401, detail="Authorization header missing")

    return await call_next(request)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(manage_patients.router, prefix="/v1/manage")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="localhost",
        port=8000
    )