from pydantic import BaseModel, Field


class EmployeeCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    role: str = Field(..., min_length=1, max_length=100)


class EmployeeResponse(BaseModel):
    id: int
    name: str
    role: str

    model_config = {"from_attributes": True}
