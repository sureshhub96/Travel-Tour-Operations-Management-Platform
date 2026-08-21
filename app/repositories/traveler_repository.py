from sqlalchemy.orm import Session

from app.models.traveler import Traveler


class TravelerRepository:

    @staticmethod
    def create(
        db: Session,
        traveler: Traveler
    ):

        db.add(traveler)
        db.commit()
        db.refresh(traveler)

        return traveler

    @staticmethod
    def get_by_id(
        db: Session,
        traveler_id: int
    ):

        return db.query(Traveler).filter(
            Traveler.id == traveler_id
        ).first()

    @staticmethod
    def get_by_booking(
        db: Session,
        booking_id: int
    ):

        return db.query(Traveler).filter(
            Traveler.booking_id == booking_id
        ).all()

    @staticmethod
    def get_by_passport(
        db: Session,
        passport_number: str
    ):

        return db.query(Traveler).filter(
            Traveler.passport_number ==
            passport_number
        ).first()