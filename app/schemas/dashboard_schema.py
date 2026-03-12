from pydantic import BaseModel

class DashboardSummaryResponse(BaseModel):
    total_employees: int
    total_attendance_records: int
    present_today: int
    absent_today: int
