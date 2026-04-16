from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite file-based database stored in the project folder
DATABASE_URL = "sqlite:///./employees.db"

# Engine is the connection to the database
# check_same_thread=False is required for SQLite with FastAPI
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

# SessionLocal handles individual database transactions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base is inherited by all models (tables)
Base = declarative_base()


# Dependency injected into routes to get a DB session
# Automatically closes the session after the request is done
def get_db():
    db = SessionLocal()
    try:
        yield db       # Provide the session to the route
    finally:
        db.close()     # Always close after use
