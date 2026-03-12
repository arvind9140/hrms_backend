from fastapi import APIRouter, status, Query
from app.schemas.attendance_schema import AttendanceCreate, AttendanceUpdate, AttendanceResponse
from app.services.attendance_service import AttendanceService
from typing import List, Optional

router = APIRouter(prefix="/attendance", tags=["Attendance"])

@router.post("", response_model=AttendanceResponse, status_code=status.HTTP_201_CREATED)
async def mark_attendance(attendance: AttendanceCreate):
    return await AttendanceService.mark_attendance(attendance)

@router.put("/{record_id}", response_model=AttendanceResponse)
async def update_attendance(record_id: str, attendance: AttendanceUpdate):
    return await AttendanceService.update_attendance(record_id, attendance)

@router.get("", response_model=List[AttendanceResponse])
async def get_attendance():
    return await AttendanceService.get_all_attendance()

@router.get("/employee/{employee_id}", response_model=List[AttendanceResponse])
async def get_attendance_by_employee(employee_id: str):
    return await AttendanceService.get_by_employee(employee_id)

@router.get("/date", response_model=List[AttendanceResponse])
async def get_attendance_by_date(date: str = Query(..., description="Date in YYYY-MM-DD format")):
    return await AttendanceService.get_by_date(date)

@router.get("/filter", response_model=List[AttendanceResponse])
async def filter_attendance(
    start_date: str = Query(..., description="Start Date in YYYY-MM-DD format"),
    end_date: str = Query(..., description="End Date in YYYY-MM-DD format")
):
    return await AttendanceService.filter_by_date_range(start_date, end_date)
