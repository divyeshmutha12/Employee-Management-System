from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import engine, Base, get_db
from schemas import EmployeeCreate, EmployeeResponse
from typing import List
import models  # Importing models so SQLAlchemy knows about them

# Creates tables in SQLite if they don't already exist
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Employee Management System")

# Allow frontend requests from local React dev servers
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_origin_regex=r"https?://(localhost|127\.0\.0\.1)(:\d+)?$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "Welcome to the Employee Management System"}


# ---------- CREATE ----------
@app.post("/employees", response_model=EmployeeResponse)
def add_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    # Build a new Employee record from the request data
    new_employee = models.Employee(name=employee.name, role=employee.role)
    db.add(new_employee)      # Stage the new record
    db.commit()               # Save to database
    db.refresh(new_employee)  # Reload to get the auto-generated id
    return new_employee


# ---------- READ ----------
@app.get("/employees", response_model=List[EmployeeResponse])
def get_all_employees(db: Session = Depends(get_db)):
    # Fetch every row from the employees table
    employees = db.query(models.Employee).all()
    return employees


# ---------- DELETE ----------
@app.delete("/employees/{employee_id}")
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    # Look up the employee by primary key
    employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()

    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    db.delete(employee)  # Mark for deletion
    db.commit()          # Apply the deletion
    return {"message": f"Employee {employee_id} deleted successfully"}
