from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database import get_db
from app.models.user import User

from app.schemas.traveler import (
    TravelerCreate,
    TravelerResponse,
    TravelerUpdate
)

from app.services.traveler_service import (
    TravelerService
)


router = APIRouter(
    tags=["Travelers"]
)


@router.post(
    "/bookings/{booking_id}/travelers",
    response_model=TravelerResponse,
    status_code=201
)
def create_traveler(
    booking_id: int,
    traveler: TravelerCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return TravelerService.create(
        db,
        booking_id,
        traveler
    )


@router.get(
    "/bookings/{booking_id}/travelers",
    response_model=list[TravelerResponse]
)
def get_travelers(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return TravelerService.get_by_booking(
        db,
        booking_id
    )


@router.put(
    "/travelers/{traveler_id}",
    response_model=TravelerResponse
)
def update_traveler(
    traveler_id: int,
    traveler: TravelerUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return TravelerService.update(
        db,
        traveler_id,
        traveler
    )