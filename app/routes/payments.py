from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    HTTPException,
)

from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database import get_db

from app.models.booking import Booking
from app.models.customer import Customer
from app.models.user import User

from app.schemas.payment import (
    PaymentCreate,
    PaymentResponse,
)

from app.services.payment_service import PaymentService
from app.services.booking_service import BookingService

from app.tasks.notification_tasks import (
    payment_success_task,
    payment_failure_task,
    booking_confirmation_task,
)


router = APIRouter(
    prefix="/payments",
    tags=["Payments"],
)


# =========================================================
# CREATE PAYMENT
# =========================================================

@router.post(
    "/{booking_id}",
    response_model=PaymentResponse,
    status_code=201,
)
def create_payment(
    booking_id: int,
    payment: PaymentCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    # -----------------------------------------------------
    # Check Booking
    # -----------------------------------------------------

    booking = (
        db.query(Booking)
        .filter(Booking.id == booking_id)
        .first()
    )

    if not booking:
        raise HTTPException(
            status_code=404,
            detail="Booking not found",
        )

    # -----------------------------------------------------
    # Check Customer
    # -----------------------------------------------------

    customer = (
        db.query(Customer)
        .filter(Customer.id == booking.customer_id)
        .first()
    )

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found",
        )

    # -----------------------------------------------------
    # Create Payment
    # -----------------------------------------------------

    result = PaymentService.create_payment(
        db,
        booking_id,
        payment,
    )

    # -----------------------------------------------------
    # Payment SUCCESS
    # -----------------------------------------------------

    if result.payment_status == "Success":

        # Confirm booking
        confirmed_booking = BookingService.confirm(
            db,
            booking_id,
        )

        # Payment success notification
        if customer.email:
            background_tasks.add_task(
                payment_success_task,
                customer.email,
                booking_id,
                result.amount,
            )

        # Booking confirmation notification
        if customer.email:
            background_tasks.add_task(
                booking_confirmation_task,
                customer.email,
                confirmed_booking.id,
            )

    # -----------------------------------------------------
    # Payment FAILED
    # -----------------------------------------------------

    elif result.payment_status == "Failed":

        if customer.email:
            background_tasks.add_task(
                payment_failure_task,
                customer.email,
                booking_id,
            )

    return result


# =========================================================
# GET ALL PAYMENTS
# =========================================================

@router.get(
    "",
    response_model=list[PaymentResponse],
)
def get_payments(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return PaymentService.get_all(db)


# =========================================================
# GET PAYMENT BY ID
# =========================================================

@router.get(
    "/{payment_id}",
    response_model=PaymentResponse,
)
def get_payment(
    payment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return PaymentService.get_by_id(
        db,
        payment_id,
    )


# =========================================================
# REFUND PAYMENT
# =========================================================

@router.post(
    "/{payment_id}/refund",
    response_model=PaymentResponse,
)
def refund_payment(
    payment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return PaymentService.refund(
        db,
        payment_id,
    )