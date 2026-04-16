from pydantic import BaseModel


# Schema for creating an employee (used in POST request body)
class EmployeeCreate(BaseModel):
    name: str
    role: str


# Schema for returning employee data (includes id)
class EmployeeResponse(BaseModel):
    id: int
    name: str
    role: str

    class Config:
        from_attributes = True  # Allows reading data from SQLAlchemy model objects
