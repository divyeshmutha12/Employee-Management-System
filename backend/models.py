from sqlalchemy import Column, Integer, String
from database import Base


# This class maps to the 'employees' table in the database
class Employee(Base):
    __tablename__ = "employees"  # Table name in SQLite

    id = Column(Integer, primary_key=True, index=True)  # Auto-incrementing primary key
    name = Column(String, nullable=False)               # Employee's full name
    role = Column(String, nullable=False)               # Employee's job role
