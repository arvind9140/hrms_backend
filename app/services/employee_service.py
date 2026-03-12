from app.database import get_database
from app.schemas.employee_schema import EmployeeCreate, EmployeeModel
from app.exceptions.custom_exceptions import ConflictException, NotFoundException
from datetime import datetime

class EmployeeService:
    @staticmethod
    def get_collection():
        db = get_database()
        return db.employees

    @staticmethod
    def get_attendance_collection():
        db = get_database()
        return db.attendance

    @classmethod
    async def create_employee(cls, employee_data: EmployeeCreate):
        collection = cls.get_collection()
        
        # Check if employee_id already exists
        if await collection.find_one({"employee_id": employee_data.employee_id}):
            raise ConflictException("Employee with this ID already exists.")
        
        # Check if email already exists
        if await collection.find_one({"email": employee_data.email}):
            raise ConflictException("Employee with this email already exists.")
            
        new_emp = employee_data.model_dump()
        new_emp["created_at"] = datetime.utcnow()
        
        result = await collection.insert_one(new_emp)
        new_emp["_id"] = str(result.inserted_id)
        return new_emp

    @classmethod
    async def get_all_employees(cls):
        collection = cls.get_collection()
        att_collection = cls.get_attendance_collection()
        
        employees_cursor = collection.find()
        employees = await employees_cursor.to_list(length=1000)
        
        for emp in employees:
            emp["_id"] = str(emp["_id"])
            # Calculate total_present_days
            present_count = await att_collection.count_documents({
                "employee_id": emp["employee_id"],
                "status": "Present"
            })
            emp["total_present_days"] = present_count
            
        return employees

    @classmethod
    async def get_employee_by_id(cls, employee_id: str):
        collection = cls.get_collection()
        emp = await collection.find_one({"employee_id": employee_id})
        if not emp:
            raise NotFoundException("Employee not found.")
            
        emp["_id"] = str(emp["_id"])
        
        att_collection = cls.get_attendance_collection()
        present_count = await att_collection.count_documents({
            "employee_id": emp["employee_id"],
            "status": "Present"
        })
        emp["total_present_days"] = present_count
        
        return emp

    @classmethod
    async def delete_employee(cls, employee_id: str):
        collection = cls.get_collection()
        att_collection = cls.get_attendance_collection()
        
        result = await collection.delete_one({"employee_id": employee_id})
        if result.deleted_count == 0:
            raise NotFoundException("Employee not found.")
            
        # Delete related attendance records
        await att_collection.delete_many({"employee_id": employee_id})
        return {"message": "Employee and associated attendance records deleted successfully."}
