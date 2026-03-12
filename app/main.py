from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.database import connect_to_mongo, close_mongo_connection
from app.routers import employee_router, attendance_router, dashboard_router

app = FastAPI(title="HRMS Lite API", description="API for HRMS Lite application", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(employee_router.router)
app.include_router(attendance_router.router)
app.include_router(dashboard_router.router)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    detail = exc.errors()
    message = "Validation error."

    if isinstance(detail, list) and detail:
        first = detail[0]
        field = ""
        if isinstance(first, dict):
            loc = first.get("loc", [])
            if isinstance(loc, (list, tuple)) and len(loc) >= 2:
                field = str(loc[-1])
            msg = first.get("msg", "Invalid value.")
            if field == "email":
                message = "Invalid email address."
            else:
                message = f"{field.capitalize()}: {msg}" if field else msg

    return JSONResponse(status_code=422, content={"detail": message})

@app.on_event("startup")
async def startup_db_client():
    await connect_to_mongo()

@app.on_event("shutdown")
async def shutdown_db_client():
    await close_mongo_connection()

@app.get("/")
def read_root():
    return {"message": "Welcome to HRMS Lite API"}
