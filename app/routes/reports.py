from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database import get_db
from app.models.user import User

from app.services.report_service import ReportService


router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)


# ==================================================
# DAILY BOOKING REPORT
# ==================================================

@router.get(
    "/daily-bookings"
)
def daily_booking_report(
    report_date: date | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return ReportService.daily_booking_report(
        db,
        report_date
    )


# ==================================================
# MONTHLY REVENUE REPORT
# ==================================================

@router.get(
    "/monthly-revenue"
)
def monthly_revenue_report(
    year: int = Query(
        ...,
        ge=2000,
        le=2100
    ),
    month: int = Query(
        ...,
        ge=1,
        le=12
    ),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return ReportService.monthly_revenue_report(
        db,
        year,
        month
    )


# ==================================================
# DESTINATION-WISE REVENUE
# ==================================================

@router.get(
    "/destination-revenue"
)
def destination_revenue_report(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return ReportService.destination_revenue_report(
        db
    )


# ==================================================
# PACKAGE PERFORMANCE
# ==================================================

@router.get(
    "/package-performance"
)
def package_performance_report(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return ReportService.package_performance_report(
        db
    )


# ==================================================
# CANCELLATION REPORT
# ==================================================

@router.get(
    "/cancellations"
)
def cancellation_report(
    start_date: date | None = None,
    end_date: date | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return ReportService.cancellation_report(
        db,
        start_date,
        end_date
    )


# ==================================================
# CUSTOMER BOOKING HISTORY
# ==================================================

@router.get(
    "/customer-booking-history/{customer_id}"
)
def customer_booking_history(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return ReportService.customer_booking_history(
        db,
        customer_id
    )