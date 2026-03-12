from fastapi import APIRouter
from app.schemas.dashboard_schema import DashboardSummaryResponse
from app.services.dashboard_service import DashboardService

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/summary", response_model=DashboardSummaryResponse)
async def get_dashboard_summary():
    return await DashboardService.get_summary()
