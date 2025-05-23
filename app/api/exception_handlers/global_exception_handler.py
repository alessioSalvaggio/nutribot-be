from fastapi import Request
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.responses import JSONResponse
from hypaz_core.mongo_logging import log_to_mongo
import traceback
import httpx
import os

ERROR_WEBHOOK_URL = os.getenv("ERROR_WEBHOOK_URL")

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

    if ERROR_WEBHOOK_URL and ERROR_WEBHOOK_URL != "":
        async with httpx.AsyncClient() as client:
            try:
                await client.post(ERROR_WEBHOOK_URL, json=error_log)
            except Exception as webhook_exc:
                print(f"Failed to send error to webhook: {webhook_exc}")

    return JSONResponse(
        status_code=status_code,
        content={"error": error_type, "detail": detail},
    )
