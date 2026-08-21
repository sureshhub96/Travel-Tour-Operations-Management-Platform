from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.itinerary import Itinerary
from app.models.package import TourPackage

from app.repositories.itinerary_repository import (
    ItineraryRepository,
)


class ItineraryService:

    @staticmethod
    def create(
        db: Session,
        package_id: int,
        data
    ):

        # Check package
        package = db.query(TourPackage).filter(
            TourPackage.id == package_id
        ).first()

        if not package:
            raise HTTPException(
                status_code=404,
                detail="Package not found"
            )

        # Check day number
        if data.day_number > package.duration_days:

            raise HTTPException(
                status_code=400,
                detail=(
                    "Day number cannot exceed "
                    "package duration"
                )
            )

        # Check duplicate day
        existing = db.query(Itinerary).filter(
            Itinerary.package_id == package_id,
            Itinerary.day_number == data.day_number
        ).first()

        if existing:

            raise HTTPException(
                status_code=400,
                detail=(
                    "This day number already exists "
                    "for this package"
                )
            )

        itinerary = Itinerary(
            package_id=package_id,
            **data.model_dump()
        )

        try:

            return ItineraryRepository.create(
                db,
                itinerary
            )

        except IntegrityError:

            db.rollback()

            raise HTTPException(
                status_code=400,
                detail="Duplicate itinerary day"
            )

    @staticmethod
    def get_by_package(
        db: Session,
        package_id: int
    ):

        package = db.query(TourPackage).filter(
            TourPackage.id == package_id
        ).first()

        if not package:

            raise HTTPException(
                status_code=404,
                detail="Package not found"
            )

        return ItineraryRepository.get_by_package(
            db,
            package_id
        )

    @staticmethod
    def get(
        db: Session,
        itinerary_id: int
    ):

        itinerary = ItineraryRepository.get_by_id(
            db,
            itinerary_id
        )

        if not itinerary:

            raise HTTPException(
                status_code=404,
                detail="Itinerary not found"
            )

        return itinerary

    @staticmethod
    def update(
        db: Session,
        itinerary_id: int,
        data
    ):

        itinerary = ItineraryService.get(
            db,
            itinerary_id
        )

        package = db.query(TourPackage).filter(
            TourPackage.id == itinerary.package_id
        ).first()

        update_data = data.model_dump(
            exclude_unset=True
        )

        new_day = update_data.get(
            "day_number",
            itinerary.day_number
        )

        if new_day > package.duration_days:

            raise HTTPException(
                status_code=400,
                detail=(
                    "Day number cannot exceed "
                    "package duration"
                )
            )

        # Check duplicate day
        if new_day != itinerary.day_number:

            duplicate = db.query(Itinerary).filter(
                Itinerary.package_id ==
                itinerary.package_id,
                Itinerary.day_number == new_day,
                Itinerary.id != itinerary.id
            ).first()

            if duplicate:

                raise HTTPException(
                    status_code=400,
                    detail=(
                        "This day number already exists "
                        "for this package"
                    )
                )

        # Validate time if times are updated
        start_time = update_data.get(
            "start_time",
            itinerary.start_time
        )

        end_time = update_data.get(
            "end_time",
            itinerary.end_time
        )

        if end_time <= start_time:

            raise HTTPException(
                status_code=400,
                detail="End time must be after start time"
            )

        for key, value in update_data.items():
            setattr(itinerary, key, value)

        db.commit()
        db.refresh(itinerary)

        return itinerary

    @staticmethod
    def delete(
        db: Session,
        itinerary_id: int
    ):

        itinerary = ItineraryService.get(
            db,
            itinerary_id
        )

        ItineraryRepository.delete(
            db,
            itinerary
        )