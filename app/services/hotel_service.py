from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.destination import Destination
from app.models.hotel import Hotel


class HotelService:

    @staticmethod
    def create(
        db: Session,
        data
    ):

        destination = db.query(
            Destination
        ).filter(
            Destination.id == data.destination_id
        ).first()

        if not destination:
            raise HTTPException(
                status_code=404,
                detail="Destination not found"
            )

        hotel = Hotel(
            **data.model_dump()
        )

        db.add(hotel)
        db.commit()
        db.refresh(hotel)

        return hotel

    @staticmethod
    def get_all(
        db: Session
    ):

        return db.query(Hotel).all()