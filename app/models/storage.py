import uuid
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.db.session import Base

class StorageDevice(Base):
    
    __tablename__ = "storage_devices"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    user_id = Column(
        UUID(as_uuid=True), 
        ForeignKey("users.id", ondelete="CASCADE"), 
        nullable=False
    )
    
    model = Column(String, nullable=False)           # Example: "Western Digital Red Plus"
    serial_number = Column(String, unique=True)      # Serial number
    capacity_gb = Column(Integer, nullable=False)    # Capacity
    status = Column(String, default="active")        # SMART Status: active, faulty, replacement
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
    
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    def __repr__(self):
        return f"<StorageDevice(model={self.model}, sn={self.serial_number}, user_id={self.user_id})>"