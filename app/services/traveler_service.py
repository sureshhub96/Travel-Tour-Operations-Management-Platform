from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.booking import Booking
from app.models.traveler import Traveler

from app.repositories.traveler_repository import (
    TravelerRepository
)


class TravelerService:

    @staticmethod
    def create(
        db: Session,
        booking_id: int,
        data
    ):

        # Check booking
        booking = db.query(Booking).filter(
            Booking.id == booking_id
        ).first()

        if not booking:

            raise HTTPException(
                status_code=404,
                detail="Booking not found"
            )

        # Don't allow travelers for cancelled bookings
        if booking.booking_status == "Cancelled":

            raise HTTPException(
                status_code=400,
                detail=(
                    "Cannot add traveler to "
                    "cancelled booking"
                )
            )

        # Get existing travelers
        existing_count = db.query(
            Traveler
        ).filter(
            Traveler.booking_id == booking_id
        ).count()

        # Prevent exceeding booking traveler count
        if existing_count >= booking.number_of_travelers:

            raise HTTPException(
                status_code=400,
                detail=(
                    "Traveler count cannot exceed "
                    "number of travelers in booking"
                )
            )

        # Check passport
        if data.passport_number:

            existing_passport = (
                TravelerRepository.get_by_passport(
                    db,
                    data.passport_number
                )
            )

            if existing_passport:

                raise HTTPException(
                    status_code=400,
                    detail="Passport number already exists"
                )

        traveler = Traveler(
            booking_id=booking_id,
            **data.model_dump()
        )

        return TravelerRepository.create(
            db,
            traveler
        )

    @staticmethod
    def get_by_booking(
        db: Session,
        booking_id: int
    ):

        booking = db.query(Booking).filter(
            Booking.id == booking_id
        ).first()

        if not booking:

            raise HTTPException(
                status_code=404,
                detail="Booking not found"
            )

        return TravelerRepository.get_by_booking(
            db,
            booking_id
        )

    @staticmethod
    def update(
        db: Session,
        traveler_id: int,
        data
    ):

        traveler = TravelerRepository.get_by_id(
            db,
            traveler_id
        )

        if not traveler:

            raise HTTPException(
                status_code=404,
                detail="Traveler not found"
            )

        update_data = data.model_dump(
            exclude_unset=True
        )

        # Passport validation
        if "passport_number" in update_data:

            passport = update_data["passport_number"]

            if passport:

                existing = (
                    TravelerRepository
                    .get_by_passport(
                        db,
                        passport
                    )
                )

                if existing and existing.id != traveler_id:

                    raise HTTPException(
                        status_code=400,
                        detail=(
                            "Passport number already exists"
                        )
                    )

        for key, value in update_data.items():
            setattr(traveler, key, value)

        db.commit()
        db.refresh(traveler)

        return traveler