from pydantic import BaseModel, Field
from datetime import date as dt_date, datetime as dt_datetime
from typing import Literal, Optional

class AttendanceModel(BaseModel):
    employee_id: str = Field(..., description="Employee ID")
    date: dt_date = Field(..., description="Attendance Date")
    status: Literal["Present", "Absent"] = Field(..., description="Status")
    created_at: dt_datetime = Field(default_factory=dt_datetime.utcnow)

class AttendanceCreate(BaseModel):
    employee_id: str
    date: dt_date
    status: Literal["Present", "Absent"]

class AttendanceUpdate(BaseModel):
    employee_id: str
    date: dt_date
    status: Literal["Present", "Absent"]

class AttendanceResponse(AttendanceModel):
    id: str = Field(alias="_id")
    employee_name: Optional[str] = None

    class Config:
        populate_by_name = True
        json_encoders = {dt_date: lambda v: v.isoformat(), dt_datetime: lambda v: v.isoformat()}
