from app.database import get_database
from app.schemas.attendance_schema import AttendanceCreate, AttendanceUpdate
from app.exceptions.custom_exceptions import NotFoundException, ConflictException
from datetime import datetime
from pymongo import ReturnDocument
from bson import ObjectId

class AttendanceService:
    @staticmethod
    def get_collection():
        db = get_database()
        return db.attendance
        
    @staticmethod
    def get_employee_collection():
        db = get_database()
        return db.employees

    @classmethod
    async def mark_attendance(cls, attendance_data: AttendanceCreate):
        collection = cls.get_collection()
        emp_collection = cls.get_employee_collection()
        
        # Verify employee exists
        employee = await emp_collection.find_one({"employee_id": attendance_data.employee_id})
        if not employee:
            raise NotFoundException("Employee not found.")
            
        # Convert date to string for consistent storage/querying
        record_date_str = attendance_data.date.isoformat()
        update_payload = {
            "employee_id": attendance_data.employee_id,
            "date": record_date_str,
            "status": attendance_data.status,
            "employee_name": employee.get("name"),
        }

        existing = await collection.find_one({
            "employee_id": attendance_data.employee_id,
            "date": record_date_str
        })

        if existing:
            updated = await collection.find_one_and_update(
                {"_id": existing["_id"]},
                {"$set": update_payload},
                return_document=ReturnDocument.AFTER
            )
            updated["_id"] = str(updated["_id"])
            return updated

        new_record = update_payload
        new_record["created_at"] = datetime.utcnow()
        result = await collection.insert_one(new_record)
        new_record["_id"] = str(result.inserted_id)
        return new_record

    @classmethod
    async def _format_records(cls, cursor):
        records = await cursor.to_list(length=1000)
        for record in records:
            record["_id"] = str(record["_id"])
        return records

    @classmethod
    async def update_attendance(cls, record_id: str, attendance_data: AttendanceUpdate):
        collection = cls.get_collection()
        emp_collection = cls.get_employee_collection()

        if not ObjectId.is_valid(record_id):
            raise NotFoundException("Attendance record not found.")

        existing_record = await collection.find_one({"_id": ObjectId(record_id)})
        if not existing_record:
            raise NotFoundException("Attendance record not found.")

        employee = await emp_collection.find_one({"employee_id": attendance_data.employee_id})
        if not employee:
            raise NotFoundException("Employee not found.")

        record_date_str = attendance_data.date.isoformat()
        duplicate = await collection.find_one({
            "employee_id": attendance_data.employee_id,
            "date": record_date_str,
            "_id": {"$ne": ObjectId(record_id)},
        })
        if duplicate:
            raise ConflictException("Attendance already exists for this employee and date.")

        update_payload = {
            "employee_id": attendance_data.employee_id,
            "date": record_date_str,
            "status": attendance_data.status,
            "employee_name": employee.get("name"),
        }

        updated = await collection.find_one_and_update(
            {"_id": ObjectId(record_id)},
            {"$set": update_payload},
            return_document=ReturnDocument.AFTER,
        )
        updated["_id"] = str(updated["_id"])
        return updated

    @classmethod
    async def get_all_attendance(cls):
        collection = cls.get_collection()
        cursor = collection.find().sort("date", -1)
        return await cls._format_records(cursor)

    @classmethod
    async def get_by_employee(cls, employee_id: str):
        collection = cls.get_collection()
        cursor = collection.find({"employee_id": employee_id}).sort("date", -1)
        return await cls._format_records(cursor)

    @classmethod
    async def get_by_date(cls, date: str):
        collection = cls.get_collection()
        cursor = collection.find({"date": date}).sort("employee_id", 1)
        return await cls._format_records(cursor)

    @classmethod
    async def filter_by_date_range(cls, start_date: str, end_date: str):
        collection = cls.get_collection()
        cursor = collection.find({
            "date": {"$gte": start_date, "$lte": end_date}
        }).sort("date", -1)
        return await cls._format_records(cursor)
