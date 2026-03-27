from sqlalchemy.orm import Session
from uuid import UUID
from typing import List, Tuple, Optional
from app.models.storage import StorageDevice
from app.schemas.storage import StorageCreate, StorageUpdate

class StorageService:
    model = StorageDevice

    def get(self, db: Session, id: UUID) -> Optional[StorageDevice]:
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multi_by_owner(self, db: Session, *, user_id: UUID, page: int, limit: int) -> Tuple[List[StorageDevice], int]:
        query = db.query(self.model).filter(self.model.user_id == user_id)
        total = query.count()
        items = query.offset((page - 1) * limit).limit(limit).all()
        return items, total

    def create_with_owner(self, db: Session, *, obj_in: StorageCreate, user_id: UUID) -> StorageDevice:
        obj_in_data = obj_in.model_dump()
        db_obj = self.model(**obj_in_data, user_id=user_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, *, db_obj: StorageDevice, obj_in: StorageUpdate) -> StorageDevice:
        update_data = obj_in.model_dump(exclude_unset=True)
        for field in update_data:
            setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, id: UUID) -> Optional[StorageDevice]:
        obj = db.query(self.model).filter(self.model.id == id).first()
        if obj:
            db.delete(obj)
            db.commit()
        return obj

storage_service = StorageService()