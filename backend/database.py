from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pathlib import Path
import logging

# Basic logger for database events
logger = logging.getLogger(__name__)

# Build an absolute DB path so app works from any current directory
BASE_DIR = Path(__file__).resolve().parent
DB_FILE = BASE_DIR / "employees.db"
DATABASE_URL = f"sqlite:///{DB_FILE.as_posix()}"

# Engine is the connection to the database
# check_same_thread=False is required for SQLite with FastAPI
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

# SessionLocal handles individual database transactions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base is inherited by all models (tables)
Base = declarative_base()

logger.info("SQLite database configured at %s", DB_FILE)


# Dependency injected into routes to get a DB session
# Automatically closes the session after the request is done
def get_db():
    db = SessionLocal()
    try:
        yield db       # Provide the session to the route
    finally:
        db.close()     # Always close after use
