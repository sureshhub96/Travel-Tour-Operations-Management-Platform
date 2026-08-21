from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.hotel import Hotel
from app.models.room import Room


class RoomService:

    @staticmethod
    def create(
        db: Session,
        data
    ):

        hotel = db.query(Hotel).filter(
            Hotel.id == data.hotel_id
        ).first()

        if not hotel:
            raise HTTPException(
                status_code=404,
                detail="Hotel not found"
            )

        existing = db.query(Room).filter(
            Room.room_number == data.room_number
        ).first()

        if existing:
            raise HTTPException(
                status_code=400,
                detail="Room number already exists"
            )

        room = Room(
            **data.model_dump()
        )

        db.add(room)
        db.commit()
        db.refresh(room)

        return room

    @staticmethod
    def get_by_hotel(
        db: Session,
        hotel_id: int
    ):

        hotel = db.query(Hotel).filter(
            Hotel.id == hotel_id
        ).first()

        if not hotel:
            raise HTTPException(
                status_code=404,
                detail="Hotel not found"
            )

        return db.query(Room).filter(
            Room.hotel_id == hotel_id
        ).all()