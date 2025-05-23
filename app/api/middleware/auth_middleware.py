from fastapi import Request, HTTPException

from fastapi.security import APIKeyHeader
from firebase_admin import auth
import os

# Define bearer token
api_key_scheme = APIKeyHeader(name="Authorization", auto_error=False)

async def auth_middleware(request: Request, call_next):
    try:
        port = request.url.port
        
        if request.url.path.startswith("/docs") or request.url.path.startswith("/openapi.json"):
            return await call_next(request)
        jwt_token = request.headers.get("Authorization")
         
        if jwt_token:
            if jwt_token == os.getenv("OVERRIDE_API_AUTH_TOKEN"):
                request.state.user_id = "OVERRIDE_USER"
                request.state.email = "alessio.salvaggio@outlook.com"
                return await call_next(request)
            else:
                try:
                    decoded_token = auth.verify_id_token(jwt_token)
                    request.state.user_id = decoded_token["uid"]
                    request.state.email = decoded_token["email"]
                except Exception:
                    raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        else:
            raise HTTPException(status_code=401, detail="Authorization header missing")

        return await call_next(request)
    except Exception as e:
        raise e
