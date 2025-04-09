import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, Request, HTTPException
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.api.endpoints.manage_patients import router as patient_manager_router
from app.api.endpoints.manage_measurements import router as measurements_manager_router
from app.api.endpoints.manage_payments import router as payments_router
from app.api.endpoints.webhooks import router as webhook_router
import firebase_admin
from firebase_admin import auth, credentials
from app.core.mongo_core import MongoCore
from app.core.mongo_logging import log_to_mongo 
from app.config.generic_conf import DEV_PORT, DEV_USERS
import traceback
import httpx

ERROR_WEBHOOK_URL = os.getenv("ERROR_WEBHOOK_URL")  # URL del webhook centralizzato

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

def convert_bytes_to_strings(d):
    if isinstance(d, dict):
        return {key: convert_bytes_to_strings(value) for key, value in d.items()}
    elif isinstance(d, list):
        return [convert_bytes_to_strings(item) for item in d]
    elif isinstance(d, (bytes, bytearray)):
        return d.decode('utf-8', errors='ignore')  # You can change 'utf-8' to another encoding if needed
    else:
        return d

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handles all exceptions dynamically, logs them, and triggers a webhook."""
    
    error_type = type(exc).__name__
    status_code = 500
    detail = "An unexpected error occurred"
    
    if isinstance(exc, RequestValidationError):
        status_code = 422
        detail = exc.errors()
    elif isinstance(exc, StarletteHTTPException):
        status_code = exc.status_code
        detail = exc.detail

    # Collect request metadata dynamically
    request_metadata = {
        "method": request.method,
        "url": str(request.url),
        "headers": dict(request.headers),
        "client": request.client.host if request.client else "unknown",
    }

    error_log = {
        "error_type": error_type,
        "status_code": status_code,
        "detail": detail,
        "traceback": traceback.format_exc(),
        "request": request_metadata,
    }

    # Log the error
    await log_to_mongo(
        "API_ERROR_HANDLER", 
        "app/main/global_exception_handler", 
        "ERROR", 
        str(error_log)
    )

    if ERROR_WEBHOOK_URL:
        async with httpx.AsyncClient() as client:
            try:
                await client.post(ERROR_WEBHOOK_URL, json=error_log)
            except Exception as webhook_exc:
                print(f"Failed to send error to webhook: {webhook_exc}")

    return JSONResponse(
        status_code=status_code,
        content={"error": error_type, "detail": detail},
    )

@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    try:
        port = request.url.port
        
        if request.url.path.startswith("/docs") or request.url.path.startswith("/openapi.json"):
            return await call_next(request)
        jwt_token = request.headers.get("Authorization")
         
        if jwt_token:
            # STANDARD AUTH FLOW
            if port == DEV_PORT and jwt_token == os.getenv("OVERRIDE_API_AUTH_TOKEN"):
                request.state.user_id = "OVERRIDE_USER"
                return await call_next(request)
            else:
                try:
                    decoded_token = auth.verify_id_token(jwt_token)
                    request.state.user_id = decoded_token["uid"]
                    if port == DEV_PORT and not request.state.user_id in DEV_USERS:
                        raise HTTPException(status_code=401, detail="DEV Env can be accessed only using DEV_USER jwt token")
                except Exception as e:
                    raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        else:
            raise HTTPException(status_code=401, detail="Authorization header missing")

        return await call_next(request)
    except Exception as e:
        raise e

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(patient_manager_router, prefix="/v1/patients")
app.include_router(measurements_manager_router, prefix="/v1/measurements")
app.include_router(payments_router, prefix="/v1/payments")
app.include_router(webhook_router, prefix="/v1/webhooks")

print(app.routes)
for route in app.routes:
    print(f"Route: {route.path}, Methods: {route.methods}")

# # COMMENT THIS WHEN DEV IS COMPLETED
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(
#         app,
#         host="localhost",
#         port=8001 # KEEP 8000 FOR DEV
#     )