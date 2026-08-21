from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database import get_db
from app.models.user import User

from app.schemas.hotel_reservation import (
    HotelReservationCreate,
    HotelReservationResponse,
)

from app.services.hotel_reservation_service import (
    HotelReservationService,
)


router = APIRouter(
    prefix="/hotel-reservations",
    tags=["Hotel Reservations"]
)


# ==================================================
# CREATE HOTEL RESERVATION
# ==================================================

@router.post(
    "",
    response_model=HotelReservationResponse,
    status_code=201
)
def create_hotel_reservation(
    reservation: HotelReservationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return HotelReservationService.create(
        db,
        reservation
    )


# ==================================================
# GET ALL HOTEL RESERVATIONS
# ==================================================

@router.get(
    "",
    response_model=list[HotelReservationResponse]
)
def get_hotel_reservations(
    booking_id: int | None = Query(
        None,
        ge=1
    ),
    room_id: int | None = Query(
        None,
        ge=1
    ),
    page: int = Query(
        1,
        ge=1
    ),
    limit: int = Query(
        10,
        ge=1,
        le=100
    ),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return HotelReservationService.get_all(
    db,
    booking_id=booking_id,
    room_id=room_id,
    page=page,
    limit=limit
)


# ==================================================
# GET RESERVATION BY ID
# ==================================================

@router.get(
    "/{reservation_id}",
    response_model=HotelReservationResponse
)
def get_hotel_reservation(
    reservation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return HotelReservationService.get(
        db,
        reservation_id
    )


# ==================================================
# CANCEL HOTEL RESERVATION
# ==================================================

@router.put(
    "/{reservation_id}/cancel",
    response_model=HotelReservationResponse
)
def cancel_hotel_reservation(
    reservation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return HotelReservationService.cancel(
        db,
        reservation_id
    )