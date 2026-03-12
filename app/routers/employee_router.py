from fastapi import APIRouter, status
from app.schemas.employee_schema import EmployeeCreate, EmployeeResponse
from app.services.employee_service import EmployeeService
from typing import List

router = APIRouter(prefix="/employees", tags=["Employees"])

@router.post("", response_model=EmployeeResponse, status_code=status.HTTP_201_CREATED)
async def create_employee(employee: EmployeeCreate):
    return await EmployeeService.create_employee(employee)

@router.get("", response_model=List[EmployeeResponse])
async def get_employees():
    return await EmployeeService.get_all_employees()

@router.get("/{employee_id}", response_model=EmployeeResponse)
async def get_employee(employee_id: str):
    return await EmployeeService.get_employee_by_id(employee_id)

@router.delete("/{employee_id}", status_code=status.HTTP_200_OK)
async def delete_employee(employee_id: str):
    return await EmployeeService.delete_employee(employee_id)
