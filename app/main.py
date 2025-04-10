import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from app.api.endpoints.manage_patients import router as patient_manager_router
from app.api.endpoints.manage_measurements import router as measurements_manager_router
from app.api.endpoints.manage_payments import router as payments_router
from app.api.webhooks.webhooks import router as webhook_router
from app.api.middleware.auth_middleware import auth_middleware
from app.api.exception_handlers.global_exception_handler import global_exception_handler
from app.api.middleware.cors_middleware import add_cors_middleware
import firebase_admin
from firebase_admin import credentials
from app.core.mongo_core import MongoCore
from app.core.lifespan import lifespan

# Init Variables
mongo = MongoCore()
cred_path = os.getenv("FIREBASE_CREDENTIALS_PATH")
if not cred_path:
    raise ValueError("FIREBASE_CREDENTIALS_PATH environment variable not set")
cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred)

# Run App
app = FastAPI(root_path="/nutribot/api", lifespan=lifespan)

# Add Middleware and Exception Handlers
app.exception_handler(Exception)(global_exception_handler)
app.middleware("http")(auth_middleware)
add_cors_middleware(app)

# Include Routers
app.include_router(patient_manager_router, prefix="/v1/patients")
app.include_router(measurements_manager_router, prefix="/v1/measurements")
app.include_router(payments_router, prefix="/v1/payments")
app.include_router(webhook_router, prefix="/v1/webhooks")

# COMMENT THIS WHEN DEV IS COMPLETED
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="localhost",
        port=8001 # KEEP 8000 FOR DEV
    )