from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database import get_db
from app.models.user import User

from app.schemas.hotel import (
    HotelCreate,
    HotelResponse
)

from app.schemas.room import (
    RoomCreate,
    RoomResponse
)

from app.schemas.hotel_reservation import (
    HotelReservationCreate,
    HotelReservationResponse
)

from app.services.hotel_service import HotelService
from app.services.room_service import RoomService
from app.services.hotel_reservation_service import (
    HotelReservationService
)


router = APIRouter(
    tags=["Hotels"]
)


# -------------------------
# Hotels
# -------------------------

@router.post(
    "/hotels",
    response_model=HotelResponse,
    status_code=201
)
def create_hotel(
    hotel: HotelCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return HotelService.create(
        db,
        hotel
    )


@router.get(
    "/hotels",
    response_model=list[HotelResponse]
)
def get_hotels(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return HotelService.get_all(db)


# -------------------------
# Rooms
# -------------------------

@router.post(
    "/rooms",
    response_model=RoomResponse,
    status_code=201
)
def create_room(
    room: RoomCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return RoomService.create(
        db,
        room
    )


@router.get(
    "/hotels/{hotel_id}/rooms",
    response_model=list[RoomResponse]
)
def get_hotel_rooms(
    hotel_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return RoomService.get_by_hotel(
        db,
        hotel_id
    )


# -------------------------
# Hotel Reservations
# -------------------------

@router.post(
    "/hotel-reservations",
    response_model=HotelReservationResponse,
    status_code=201
)
def create_hotel_reservation(
    reservation: HotelReservationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return HotelReservationService.create(
        db,
        reservation
    )


@router.get(
    "/hotel-reservations",
    response_model=list[HotelReservationResponse]
)
def get_hotel_reservations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return HotelReservationService.get_all(db)