from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database import get_db
from app.models.user import User

from app.schemas.cancellation import (
    CancellationCreate,
    CancellationResponse
)

from app.services.cancellation_service import (
    CancellationService
)


router = APIRouter(
    prefix="/bookings",
    tags=["Cancellation & Refund"]
)


@router.post(
    "/{booking_id}/cancel",
    response_model=CancellationResponse
)
def cancel_booking(
    booking_id: int,
    data: CancellationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return CancellationService.cancel_booking(
        db,
        booking_id,
        data
    )


@router.get(
    "/cancellations",
    response_model=list[CancellationResponse]
)
def get_cancellations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return CancellationService.get_all(db)