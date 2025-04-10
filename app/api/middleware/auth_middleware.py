from fastapi import Request, HTTPException
from firebase_admin import auth
import os
from app.config.generic_conf import DEV_PORT, DEV_USERS

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
                    if port == DEV_PORT and request.state.user_id not in DEV_USERS:
                        raise HTTPException(status_code=401, detail="DEV Env can be accessed only using DEV_USER jwt token")
                except Exception:
                    raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        else:
            raise HTTPException(status_code=401, detail="Authorization header missing")

        return await call_next(request)
    except Exception as e:
        raise e
