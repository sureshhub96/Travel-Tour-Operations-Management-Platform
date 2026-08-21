from sqlalchemy.orm import Session

from app.models.itinerary import Itinerary


class ItineraryRepository:

    @staticmethod
    def create(
        db: Session,
        itinerary: Itinerary
    ):

        db.add(itinerary)
        db.commit()
        db.refresh(itinerary)

        return itinerary

    @staticmethod
    def get_by_id(
        db: Session,
        itinerary_id: int
    ):

        return db.query(Itinerary).filter(
            Itinerary.id == itinerary_id
        ).first()

    @staticmethod
    def get_by_package(
        db: Session,
        package_id: int
    ):

        return (
            db.query(Itinerary)
            .filter(
                Itinerary.package_id == package_id
            )
            .order_by(
                Itinerary.day_number
            )
            .all()
        )

    @staticmethod
    def delete(
        db: Session,
        itinerary: Itinerary
    ):

        db.delete(itinerary)
        db.commit()