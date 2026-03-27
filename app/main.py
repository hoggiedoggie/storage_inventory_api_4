from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from app.api.v1.api import api_router
from app.core.config import settings

from app.db.session import engine, Base 
from app.models.user import User    
from app.models.storage import StorageDevice 

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Automated API documentation for Storage Inventory Project (Labs 2-4)",
    docs_url=settings.DOCS_URL,
    openapi_url=settings.OPENAPI_URL, 
    redoc_url=None 
)
def custom_openapi():
    """
    Extends the auto-generated OpenAPI schema to include security schemes.
    Requirement: Configure Swagger UI for Cookie/JWT Authentication.
    """
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "CookieAuth": {
            "type": "apiKey",
            "in": "cookie",
            "name": "access_token",
            "description": "JWT Token stored in HttpOnly cookie. Use 'Bearer <token>' format."
        }
    }
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

app.include_router(api_router, prefix="/api/v1")

@app.get("/", tags=["Root"])
def read_root():
    """
    Health check and project metadata endpoint.
    Useful for checking current environment and documentation status.
    """
    return {
        "project": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "environment": settings.APP_ENV,
        "docs_available": settings.SHOW_DOCS,
        "docs_path": settings.DOCS_URL if settings.SHOW_DOCS else "Disabled in production"
    }