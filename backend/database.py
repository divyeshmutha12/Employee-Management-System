from pathlib import Path
import logging
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Basic logger for database events
logger = logging.getLogger(__name__)

# Build an absolute DB path so app works from any current directory
BASE_DIR = Path(__file__).resolve().parent
DB_FILE = BASE_DIR / "employees.db"
DATABASE_URL = f"sqlite:///{DB_FILE.as_posix()}"

# check_same_thread=False is required when using SQLite with FastAPI
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

logger.info("SQLite database configured at %s", DB_FILE)


def get_db():
    """Yield a database session and close it when the request is done."""
    db = SessionLocal()
    try:
        yield db
    except Exception:
        # Roll back the active transaction before re-raising the error
        db.rollback()
        logger.exception("Database session failed during request")
        raise
    finally:
        try:
            db.close()
        except Exception:
            logger.exception("Failed to close database session")
