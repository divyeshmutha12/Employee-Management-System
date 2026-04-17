import logging
from typing import List

import models
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from database import engine, Base, get_db
from schemas import EmployeeCreate, EmployeeResponse

# Configure simple app-wide logs
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)

# Creates tables in SQLite if they don't already exist
try:
    Base.metadata.create_all(bind=engine)

    # Ensure soft-delete column exists for old databases created before this change
    with engine.connect() as conn:
        columns = conn.execute(text("PRAGMA table_info(employees)")).fetchall()
        column_names = {col[1] for col in columns}
        if "is_delete" not in column_names:
            conn.execute(text("ALTER TABLE employees ADD COLUMN is_delete INTEGER NOT NULL DEFAULT 0"))
            conn.commit()
            logger.info("Added missing is_delete column to employees table")

    logger.info("Database tables checked/created successfully")
except Exception:
    logger.exception("Failed to initialize database tables")
    raise

app = FastAPI(title="Employee Management System")

# Allow requests from local React development servers
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    # Covers localhost with any dev port (5174, 5175, etc.)
    allow_origin_regex=r"https?://(localhost|127\.0\.0\.1)(:\d+)?$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    logger.info("Root endpoint called")
    return {"message": "Welcome to the Employee Management System"}


# ---------- CREATE ----------
@app.post("/employees", response_model=EmployeeResponse)
def add_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    try:
        # Build and save a new employee record
        new_employee = models.Employee(name=employee.name, role=employee.role)
        db.add(new_employee)
        db.flush()
        db.commit()
        logger.info("Employee created with id=%s", new_employee.id)
        return new_employee
    except SQLAlchemyError:
        logger.exception("Database error while creating employee")
        raise HTTPException(status_code=500, detail="Failed to create employee")
    except Exception:
        logger.exception("Unexpected error while creating employee")
        raise HTTPException(status_code=500, detail="Unexpected server error")


# ---------- READ ----------
@app.get("/employees", response_model=List[EmployeeResponse])
def get_all_employees(db: Session = Depends(get_db)):
    try:
        # Fetch only active (not soft-deleted) employees
        employees = db.query(models.Employee).filter(models.Employee.is_delete == 0).all()
        logger.info("Fetched %s employees", len(employees))
        return employees
    except SQLAlchemyError:
        logger.exception("Database error while fetching employees")
        raise HTTPException(status_code=500, detail="Failed to fetch employees")
    except Exception:
        logger.exception("Unexpected error while fetching employees")
        raise HTTPException(status_code=500, detail="Unexpected server error")


# ---------- DELETE ----------
@app.delete("/employees/{employee_id}")
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    try:
        # Find active employee by ID
        employee = (
            db.query(models.Employee)
            .filter(models.Employee.id == employee_id, models.Employee.is_delete == 0)
            .first()
        )

        if not employee:
            logger.warning("Delete requested for missing employee id=%s", employee_id)
            raise HTTPException(status_code=404, detail="Employee not found")

        # Soft delete: mark row as deleted instead of removing it
        employee.is_delete = 1
        db.flush()
        db.commit()
        logger.info("Employee soft-deleted id=%s", employee_id)
        return {"message": f"Employee {employee_id} deleted successfully"}
    except HTTPException:
        raise
    except SQLAlchemyError:
        logger.exception("Database error while deleting employee id=%s", employee_id)
        raise HTTPException(status_code=500, detail="Failed to delete employee")
    except Exception:
        logger.exception("Unexpected error while deleting employee id=%s", employee_id)
        raise HTTPException(status_code=500, detail="Unexpected server error")
