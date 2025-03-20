import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, Request, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.api.endpoints import manage_patients
import firebase_admin
from firebase_admin import auth, credentials
from app.core.mongo_core import MongoCore
from app.core.mongo_logging import log_to_mongo 

cred_path = os.getenv("FIREBASE_CREDENTIALS_PATH")
if not cred_path:
    raise ValueError("FIREBASE_CREDENTIALS_PATH environment variable not set")
cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred)

mongo = MongoCore()
@asynccontextmanager
async def lifespan(app: FastAPI):
    await mongo._connect()
    print("Connected to MongoDB.")
    yield
    if mongo.client:
        mongo.client.close()
        print("MongoDB connection closed.")
        
app = FastAPI(
    root_path="/nutribot/api",
    title="Nutribot API",
    description="API per la gestione di Nutribot con autenticazione Firebase e API Key",
    version="0.2.4"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    try:
        if request.url.path.startswith("/docs") or request.url.path.startswith("/openapi.json"):
            return await call_next(request)
        
        jwt_token = request.headers.get("Authorization")
        if jwt_token:
            if jwt_token == os.getenv("OVERRIDE_API_AUTH_TOKEN"):
                request.state.user_id = "DEV_USER"
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
    except HTTPException as e:
        await log_to_mongo(
            f"MIDDLEWARE - {request.state.user_id if hasattr(request.state, "user_id") else "UNAUTH_USER"}", 
            "app/main/auth_middleware", 
            "ERROR", 
            f"{e}"
        )
        raise e

def convert_bytes_to_strings(d):
    if isinstance(d, dict):
        # If it's a dictionary, iterate through its keys and values
        return {key: convert_bytes_to_strings(value) for key, value in d.items()}
    elif isinstance(d, list):
        # If it's a list, iterate through its elements
        return [convert_bytes_to_strings(item) for item in d]
    elif isinstance(d, (bytes, bytearray)):
        # If the value is bytes or bytearray, decode it to string
        return d.decode('utf-8', errors='ignore')  # You can change 'utf-8' to another encoding if needed
    else:
        # If it's not bytes, return the value as it is
        return d

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # Log dell'errore
    desired_keys = ['base_url', 'client', 'headers', 'cookies', 'method', 'path_params', 'url', '_json']
    request_metadata = {
        k: getattr(request, k)() if callable(getattr(request, k)) else getattr(request, k)
        for k in desired_keys
        if hasattr(request, k)
    }
    
    request_metadata = convert_bytes_to_strings(request_metadata)
    
    request_metadata['base_url'] = {
        k:getattr(request_metadata['base_url'], k) for k in [
            'fragment', 'hostname', 'is_secure', 'netloc', 'password', 'path', 'port', 'query', 'scheme', 'username'
        ]
    }
    request_metadata['client'] = {
        k:getattr(request_metadata['client'], k) for k in [
            'host', 'port'
        ]
    }
    request_metadata['url'] = {
        k:getattr(request_metadata['url'], k) for k in [
            'fragment', 'hostname', 'is_secure', 'netloc', 'password', 'path', 'port', 'query', 'scheme', 'username'
        ]
    }
    request_metadata['headers'] = [[k.decode('utf-8', errors='ignore') for k in l] for l in request_metadata['headers'].raw]
    
    content = {
        "request": request_metadata,
        "error_details": exc.errors()
    }
    await log_to_mongo(
        "API_RESPONSE_ERROR_MONITOR", 
        "app/main/validation_exception_handler", 
        "ERROR", 
        f"{content}"
    )
    
    return exc

app.include_router(manage_patients.router, prefix="/v1/manage")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="localhost",
        port=8000
    )