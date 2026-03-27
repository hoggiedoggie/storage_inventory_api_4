import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator
from typing import Optional

class Settings(BaseSettings):

    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    DB_HOST: str
    DB_PORT: int = 5432
    PROJECT_NAME: str = "Storage Inventory API"
    VERSION: str = "1.0.0"

    APP_ENV: str = "development"

    JWT_ACCESS_SECRET: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    
    @field_validator("DB_USER", "DB_PASSWORD", "DB_NAME", "DB_HOST", "JWT_ACCESS_SECRET", mode="before")
    @classmethod
    def strip_spaces(cls, v):
        if isinstance(v, str):
            return v.strip()
        return v

    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding='utf-8',
        extra='ignore'
    )

    @property
    def DATABASE_URL(self) -> str:
        url = f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        return url.strip()
    
    @property
    def SHOW_DOCS(self) -> bool:
        return self.APP_ENV.lower() == "development"

    @property
    def DOCS_URL(self) -> Optional[str]:
        return "/api/docs" if self.SHOW_DOCS else None

    @property
    def OPENAPI_URL(self) -> Optional[str]:
        return "/api/openapi.json" if self.SHOW_DOCS else None

settings = Settings()