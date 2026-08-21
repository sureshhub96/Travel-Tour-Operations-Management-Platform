from fastapi import FastAPI

from app.routes.auth import router as auth_router
from app.routes.customers import router as customer_router
from app.routes.destinations import router as destination_router
from app.routes.packages import router as package_router
from app.routes.bookings import router as booking_router
from app.routes.payments import router as payment_router
from app.routes.hotels import router as hotel_router
from app.routes.rooms import router as room_router
from app.routes.hotel_reservations import router as hotel_reservation_router
from app.routes.activities import router as activity_router
from app.routes.guides import router as guide_router
from app.routes.reports import router as report_router
from app.routes.cancellations import router as cancellation_router
from app.routes.itinerary import router as itinerary_router


app = FastAPI(
    title="Travel & Tour Operations Management Platform",
    description="Backend API for Travel and Tour Operations Management",
    version="1.0.0"
)


# ==========================================
# ROUTERS
# ==========================================

app.include_router(auth_router)

app.include_router(customer_router)
app.include_router(destination_router)
app.include_router(package_router)

app.include_router(booking_router)
app.include_router(payment_router)

app.include_router(hotel_router)
app.include_router(room_router)
app.include_router(hotel_reservation_router)

app.include_router(activity_router)
app.include_router(guide_router)

app.include_router(cancellation_router)

app.include_router(report_router)
app.include_router(itinerary_router)


# ==========================================
# ROOT
# ==========================================

@app.get("/")
def root():
    return {
        "message": "Travel & Tour Operations Management Platform API",
        "status": "running",
        "version": "1.0.0"
    }


# ==========================================
# HEALTH CHECK
# ==========================================

@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }