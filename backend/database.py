from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Absolute path ensures the DB file is always created next to this file,
# regardless of which directory uvicorn is started from
DB_PATH = Path(__file__).resolve().parent / "employees.db"
DATABASE_URL = f"sqlite:///{DB_PATH}"

# check_same_thread=False is required when using SQLite with FastAPI
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Yield a database session and close it when the request is done."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
