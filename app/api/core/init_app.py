from fastapi.openapi.utils import get_openapi
from fastapi import FastAPI

from app.core.lifespan import lifespan
from app.config.api_conf import API_ROOT_PATH

def custom_app_init():
    app = FastAPI(root_path=API_ROOT_PATH, lifespan=lifespan)
    
    def custom_openapi():
        if app.openapi_schema:
            return app.openapi_schema
        openapi_schema = get_openapi(
            title="Nutribot API",
            version="1.0.0",
            description="Nutribot Backend API",
            routes=app.routes,
        )
        openapi_schema["servers"] = [
            {
                "url": API_ROOT_PATH
            }
        ]
        openapi_schema["components"]["securitySchemes"] = {
            "ApiKeyAuth": {
                "type": "apiKey",
                "in": "header",
                "name": "Authorization"
            }
        }
        for path in openapi_schema["paths"].values():
            for method in path.values():
                method.setdefault("security", []).append({"ApiKeyAuth": []})
        
        app.openapi_schema = openapi_schema
        return app.openapi_schema

    # Custom OpenAPI Schema for FastAPI with API Key Auth and Server Root Path Configuration
    app.openapi = custom_openapi
    
    return app