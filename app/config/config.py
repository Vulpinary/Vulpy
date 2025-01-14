from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    DATABASE_URL: str = os.environ.get("DATABASE_URL", "postgresql+psycopg2://user:password@host:5432/database")
    DATABASE_ECHO: bool = False
    JWT_SECRET_KEY: str = os.environ.get("JWT_SECRET_KEY")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ACCESS_TOKEN_EXPIRE_SECONDS: int = 1800

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()