from app.database import get_database
from datetime import datetime

class DashboardService:
    @classmethod
    async def get_summary(cls):
        db = get_database()
        # Ensure we use UTC date to match how attendance is recorded (locally or UTC)
        # Assuming attendance is recorded with current local date from frontend, 
        # but to be safe we'll just query what exactly is marked for "today"
        today_str = datetime.utcnow().date().isoformat()
        
        total_employees = await db.employees.count_documents({})
        total_attendance = await db.attendance.count_documents({})
        present_today = await db.attendance.count_documents({"date": today_str, "status": "Present"})
        absent_today = await db.attendance.count_documents({"date": today_str, "status": "Absent"})
        
        return {
            "total_employees": total_employees,
            "total_attendance_records": total_attendance,
            "present_today": present_today,
            "absent_today": absent_today
        }
