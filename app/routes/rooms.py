from fastapi import (
    APIRouter,
    Depends,
    Query,
)
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database import get_db
from app.models.user import User

from app.schemas.room import (
    RoomCreate,
    RoomResponse,
    RoomUpdate,
)

from app.services.room_service import RoomService


router = APIRouter(
    prefix="/rooms",
    tags=["Rooms"]
)


# ==================================================
# CREATE ROOM
# ==================================================

@router.post(
    "",
    response_model=RoomResponse,
    status_code=201
)
def create_room(
    room: RoomCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return RoomService.create(
        db,
        room
    )


# ==================================================
# GET ALL ROOMS
# ==================================================

@router.get(
    "",
    response_model=list[RoomResponse]
)
def get_rooms(
    hotel_id: int | None = Query(
        None,
        ge=1
    ),
    room_type: str | None = None,
    availability_status: str | None = None,
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
    return RoomService.get_all(
        db,
        hotel_id=hotel_id,
        room_type=room_type,
        availability_status=availability_status,
        page=page,
        limit=limit
    )


# ==================================================
# GET ROOMS BY HOTEL
# ==================================================

@router.get(
    "/hotel/{hotel_id}",
    response_model=list[RoomResponse]
)
def get_hotel_rooms(
    hotel_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return RoomService.get_by_hotel(
        db,
        hotel_id
    )


# ==================================================
# GET ROOM BY ID
# ==================================================

@router.get(
    "/{room_id}",
    response_model=RoomResponse
)
def get_room(
    room_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return RoomService.get(
        db,
        room_id
    )


# ==================================================
# UPDATE ROOM
# ==================================================

@router.put(
    "/{room_id}",
    response_model=RoomResponse
)
def update_room(
    room_id: int,
    room: RoomUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return RoomService.update(
        db,
        room_id,
        room
    )


# ==================================================
# DELETE ROOM
# ==================================================

@router.delete(
    "/{room_id}"
)
def delete_room(
    room_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    RoomService.delete(
        db,
        room_id
    )

    return {
        "message": "Room deleted successfully"
    }