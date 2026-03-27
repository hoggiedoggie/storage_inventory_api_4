from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.services.storage import storage_service
from app.schemas.storage import (
    StorageCreate, 
    StorageUpdate, 
    StorageResponse, 
    StorageListResponse
)

router = APIRouter(tags=["Storage Management"])

@router.get(
    "/", 
    response_model=StorageListResponse,
    summary="Get all user devices",
    description="Returns a paginated list of storage devices belonging to the current authenticated user.",
    responses={
        200: {"description": "List of devices successfully retrieved"},
        401: {"description": "Unauthorized: Missing or invalid session cookie"}
    }
)
def read_devices(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    page: int = Query(1, ge=1, description="Page number starting from 1"),
    limit: int = Query(10, ge=1, le=100, description="Items per page (max 100)")
):
    items, total = storage_service.get_multi_by_owner(
        db, user_id=current_user.id, page=page, limit=limit
    )
    total_pages = (total + limit - 1) // limit
    return {
        "data": items,
        "meta": {"total": total, "page": page, "limit": limit, "totalPages": total_pages}
    }

@router.post(
    "/", 
    response_model=StorageResponse, 
    status_code=status.HTTP_201_CREATED,
    summary="Register a new device",
    description="Creates a new storage device record. The 'owner_id' is automatically assigned to the current user.",
    responses={
        201: {"description": "Device successfully created"},
        401: {"description": "Unauthorized"},
        422: {"description": "Validation Error: Check input fields format"}
    }
)
def create_device(
    obj_in: StorageCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return storage_service.create_with_owner(db, obj_in=obj_in, user_id=current_user.id)

@router.get(
    "/{id}", 
    response_model=StorageResponse,
    summary="Get device details",
    description="Retrieves full information about a specific device by its UUID. Only owners can access their devices.",
    responses={
        200: {"description": "Device found and returned"},
        401: {"description": "Unauthorized"},
        404: {"description": "Not Found: Device does not exist or belongs to another user"}
    }
)
def read_device(
    id: UUID, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    device = storage_service.get(db, id=id)
    if not device or device.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Device not found")
    return device

@router.put(
    "/{id}", 
    response_model=StorageResponse,
    summary="Update device info",
    description="Updates existing device data. Requires full object in request body.",
    responses={
        200: {"description": "Device successfully updated"},
        401: {"description": "Unauthorized"},
        404: {"description": "Device not found"},
        422: {"description": "Validation Error"}
    }
)
def update_device(
    id: UUID, 
    obj_in: StorageCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    device = storage_service.get(db, id=id)
    if not device or device.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Device not found")
    return storage_service.update(db, db_obj=device, obj_in=StorageUpdate(**obj_in.model_dump()))

@router.delete(
    "/{id}", 
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete device record",
    description="Removes the device record from the system. (Note: Implements logical/soft delete if configured).",
    responses={
        204: {"description": "Device successfully deleted"},
        401: {"description": "Unauthorized"},
        404: {"description": "Device not found"}
    }
)
def delete_device(
    id: UUID, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    device = storage_service.get(db, id=id)
    if not device or device.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Device not found")
    storage_service.remove(db, id=id)
    return None