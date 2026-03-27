from fastapi import APIRouter
from app.api.v1.endpoints import auth, storage

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth")
api_router.include_router(storage.router, prefix="/devices")