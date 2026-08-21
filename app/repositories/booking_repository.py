from sqlalchemy.orm import Session

from app.models.booking import Booking


class BookingRepository:

    @staticmethod
    def create(
        db: Session,
        booking: Booking
    ):

        db.add(booking)
        db.commit()
        db.refresh(booking)

        return booking

    @staticmethod
    def get_by_id(
        db: Session,
        booking_id: int
    ):

        return db.query(Booking).filter(
            Booking.id == booking_id
        ).first()

    @staticmethod
    def get_all(
        db: Session
    ):

        return db.query(Booking).all()