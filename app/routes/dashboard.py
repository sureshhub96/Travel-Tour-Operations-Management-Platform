from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database import get_db
from app.models.user import User

from app.schemas.dashboard import (
    DashboardSummaryResponse,
    RevenueResponse,
    BookingAnalyticsResponse,
)

from app.services.dashboard_service import (
    DashboardService
)


router = APIRouter(
    prefix="/dashboard",
    tags=["Admin Dashboard"]
)


# ==================================================
# DASHBOARD SUMMARY
# ==================================================

@router.get(
    "/summary",
    response_model=DashboardSummaryResponse
)
def dashboard_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return DashboardService.get_summary(db)


# ==================================================
# REVENUE
# ==================================================

@router.get(
    "/revenue",
    response_model=RevenueResponse
)
def dashboard_revenue(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return DashboardService.get_revenue(db)


# ==================================================
# BOOKING ANALYTICS
# ==================================================

@router.get(
    "/bookings",
    response_model=BookingAnalyticsResponse
)
def dashboard_bookings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return DashboardService.get_bookings(db)