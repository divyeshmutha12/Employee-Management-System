from pydantic import BaseModel, Field


# Schema for creating an employee (used in POST request body)
class EmployeeCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    role: str = Field(..., min_length=1, max_length=100)


# Schema for returning employee data (includes id)
class EmployeeResponse(BaseModel):
    id: int
    name: str
    role: str

    class Config:
        from_attributes = True  # Allows reading data from SQLAlchemy model objects
