import uuid
from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    email = Column(String, unique=True, index=True, nullable=False)
    
    hashed_password = Column(String, nullable=True) 
    
  
    salt = Column(String, nullable=True) 
    
    yandex_id = Column(String, unique=True, nullable=True)
    vk_id = Column(String, unique=True, nullable=True)


    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
  
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    devices = relationship("StorageDevice", backref="owner", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(email={self.email}, active={self.is_active})>"