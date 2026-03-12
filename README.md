# HRMS Lite – Backend

FastAPI backend for HRMS Lite, providing RESTful APIs for employees and attendance.

## Project Overview
The backend provides APIs to:
- Manage employee records
- Mark and update attendance
- Serve dashboard summary metrics

## Tech Stack
- FastAPI (Python)
- Motor (Async MongoDB)
- Pydantic
- MongoDB (Atlas compatible)

## Steps to Run Locally
1. Open a terminal and move into the backend folder:
   ```bash
   cd backend
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate   # Windows: .\venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file:
   ```env
   MONGODB_URI=your_mongodb_connection_string
   DATABASE_NAME=hrms_db
   ```
5. Start the server:
   ```bash
   uvicorn app.main:app --reload
   ```

## Environment Variables
| Name | Description | Example |
| --- | --- | --- |
| `MONGODB_URI` | MongoDB connection string | `mongodb+srv://...` |
| `DATABASE_NAME` | MongoDB database name | `hrms_db` |

## API Overview
**Employees**
- `POST /employees`
- `GET /employees`
- `GET /employees/{employee_id}`
- `DELETE /employees/{employee_id}`

**Attendance**
- `POST /attendance`
- `PUT /attendance/{record_id}`
- `GET /attendance`
- `GET /attendance/employee/{employee_id}`
- `GET /attendance/filter`

**Dashboard**
- `GET /dashboard/summary`

## Assumptions
- Single admin user (no authentication)
- Basic HR functionality only

## Limitations
- No role-based access control
- No pagination for large datasets

