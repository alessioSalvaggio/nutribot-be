import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.api.core.bootstrap import init_services
from app.api.core.init_app import custom_app_init
from app.api.middleware.auth_middleware import auth_middleware
from app.api.middleware.cors_middleware import add_cors_middleware
from app.api.exception_handlers.global_exception_handler import global_exception_handler
from app.api.endpoints.manage_patients import router as patient_manager_router
from app.api.endpoints.manage_measurements import router as measurements_manager_router
from app.api.endpoints.manage_payments import router as payments_router
from app.api.endpoints.manage_diets import router as diets_router
from app.api.webhooks.webhooks import router as webhook_router

# Init External Services
services = init_services()

# Initialize App
app = custom_app_init()

# Add Middleware and Exception Handlers
app.exception_handler(Exception)(global_exception_handler)
app.middleware("http")(auth_middleware)
add_cors_middleware(app)

# Include Routers
app.include_router(patient_manager_router, prefix="/v1/patients")
app.include_router(measurements_manager_router, prefix="/v1/measurements")
app.include_router(payments_router, prefix="/v1/payments")
app.include_router(webhook_router, prefix="/v1/webhooks")
app.include_router(diets_router, prefix="/v1/diets")

# # COMMENT THIS WHEN DEV IS COMPLETED
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(
#         app,
#         host="localhost",
#         port=8000 # dev 8001, prod 8000
#     )