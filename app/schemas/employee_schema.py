from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional

class EmployeeModel(BaseModel):
    employee_id: str = Field(..., description="Unique Employee ID")
    name: str = Field(..., description="Full Name")
    email: EmailStr = Field(..., description="Email Address")
    department: str = Field(..., description="Department")
    created_at: datetime = Field(default_factory=datetime.utcnow)

class EmployeeCreate(BaseModel):
    employee_id: str
    name: str
    email: EmailStr
    department: str

class EmployeeResponse(EmployeeModel):
    id: str = Field(alias="_id")
    total_present_days: Optional[int] = 0

    class Config:
        populate_by_name = True
        json_encoders = {datetime: lambda v: v.isoformat()}
