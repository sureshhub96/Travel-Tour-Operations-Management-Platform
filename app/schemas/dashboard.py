from pydantic import BaseModel


class DashboardSummaryResponse(BaseModel):
    total_customers: int
    total_packages: int
    active_tours: int
    total_bookings: int
    confirmed_bookings: int
    cancelled_bookings: int
    total_revenue: float
    total_refunds: float


class RevenueResponse(BaseModel):
    total_revenue: float
    total_refunds: float
    net_revenue: float


class BookingAnalyticsResponse(BaseModel):
    total_bookings: int
    pending_bookings: int
    confirmed_bookings: int
    cancelled_bookings: int
    completed_bookings: int