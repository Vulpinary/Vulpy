from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config.config import Settings
from app.models import Base


SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:qwerty12@localhost:5432/postgres?client_encoding=utf8"

settings = Settings()
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=settings.DATABASE_ECHO)

Base.metadata.create_all(engine)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
