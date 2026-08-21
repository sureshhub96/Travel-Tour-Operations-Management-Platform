from datetime import date

from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    HTTPException,
    Query,
)
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database import get_db

from app.models.booking import Booking
from app.models.customer import Customer
from app.models.payment import Payment
from app.models.user import User

from app.schemas.booking import (
    BookingCreate,
    BookingResponse,
)

from app.services.booking_service import BookingService

from app.tasks.notification_tasks import (
    booking_confirmation_task,
)


router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"]
)


# ==================================================
# CREATE BOOKING
# ==================================================

@router.post(
    "",
    response_model=BookingResponse,
    status_code=201
)
def create_booking(
    booking: BookingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return BookingService.create(
        db,
        booking
    )


# ==================================================
# GET BOOKINGS
# Filtering + Sorting + Pagination
# ==================================================

@router.get(
    "",
    response_model=list[BookingResponse]
)
def get_bookings(
    booking_status: str | None = None,
    payment_status: str | None = None,
    booking_date: date | None = None,

    page: int = Query(
        1,
        ge=1
    ),

    limit: int = Query(
        10,
        ge=1,
        le=100
    ),

    sort_by: str = "id",

    sort_order: str = Query(
        "asc",
        pattern="^(asc|desc)$"
    ),

    db: Session = Depends(get_db),
):
    query = db.query(Booking)

    # ==================================================
    # BOOKING STATUS
    # ==================================================

    if booking_status:
        query = query.filter(
            Booking.booking_status == booking_status
        )

    # ==================================================
    # BOOKING DATE
    # ==================================================

    if booking_date:
        query = query.filter(
            Booking.booking_date == booking_date
        )

    # ==================================================
    # PAYMENT STATUS
    # ==================================================

    if payment_status:
        query = (
            query
            .join(
                Payment,
                Payment.booking_id == Booking.id
            )
            .filter(
                Payment.payment_status == payment_status
            )
            .distinct()
        )

    # ==================================================
    # SORTING
    # ==================================================

    allowed_sort_fields = {
        "id": Booking.id,
        "booking_date": Booking.booking_date,
        "number_of_travelers": Booking.number_of_travelers,
        "base_amount": Booking.base_amount,
        "discount": Booking.discount,
        "tax": Booking.tax,
        "total_amount": Booking.total_amount,
        "booking_status": Booking.booking_status,
    }

    if sort_by not in allowed_sort_fields:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Invalid sort_by '{sort_by}'. "
                f"Allowed values: "
                f"{', '.join(allowed_sort_fields.keys())}"
            )
        )

    sort_column = allowed_sort_fields[sort_by]

    if sort_order == "desc":
        query = query.order_by(
            sort_column.desc()
        )
    else:
        query = query.order_by(
            sort_column.asc()
        )

    # ==================================================
    # PAGINATION
    # ==================================================

    offset = (page - 1) * limit

    return (
        query
        .offset(offset)
        .limit(limit)
        .all()
    )


# ==================================================
# GET SINGLE BOOKING
# ==================================================

@router.get(
    "/{booking_id}",
    response_model=BookingResponse
)
def get_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return BookingService.get(
        db,
        booking_id
    )


# ==================================================
# CONFIRM BOOKING
# Level 13 - Background Notification
# ==================================================

@router.put(
    "/{booking_id}/confirm",
    response_model=BookingResponse
)
def confirm_booking(
    booking_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # ----------------------------------------------
    # Confirm booking
    # ----------------------------------------------

    booking = BookingService.confirm(
        db,
        booking_id
    )

    # ----------------------------------------------
    # Get customer
    # ----------------------------------------------

    customer = db.query(Customer).filter(
        Customer.id == booking.customer_id
    ).first()

    # ----------------------------------------------
    # Send background notification
    # ----------------------------------------------

    if customer and customer.email:
        background_tasks.add_task(
            booking_confirmation_task,
            customer.email,
            booking.id
        )

    return booking


# ==================================================
# CANCEL BOOKING
# ==================================================

@router.put(
    "/{booking_id}/cancel"
)
def cancel_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return BookingService.cancel(
        db,
        booking_id
    )