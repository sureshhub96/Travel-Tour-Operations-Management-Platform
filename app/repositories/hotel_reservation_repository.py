from datetime import date

from sqlalchemy.orm import Session

from app.models.hotel_reservation import HotelReservation


class HotelReservationRepository:

    @staticmethod
    def create(
        db: Session,
        reservation: HotelReservation
    ):
        db.add(reservation)
        db.commit()
        db.refresh(reservation)

        return reservation

    @staticmethod
    def get_by_id(
        db: Session,
        reservation_id: int
    ):
        return db.query(
            HotelReservation
        ).filter(
            HotelReservation.id == reservation_id
        ).first()

    @staticmethod
    def get_all(
        db: Session,
        booking_id: int | None = None,
        room_id: int | None = None,
        page: int = 1,
        limit: int = 10
    ):

        query = db.query(
            HotelReservation
        )

        if booking_id is not None:
            query = query.filter(
                HotelReservation.booking_id ==
                booking_id
            )

        if room_id is not None:
            query = query.filter(
                HotelReservation.room_id ==
                room_id
            )

        return (
            query
            .offset((page - 1) * limit)
            .limit(limit)
            .all()
        )

    @staticmethod
    def get_overlapping(
        db: Session,
        room_id: int,
        check_in: date,
        check_out: date,
        exclude_id: int | None = None
    ):

        query = db.query(
            HotelReservation
        ).filter(
            HotelReservation.room_id == room_id,
            HotelReservation.check_in < check_out,
            HotelReservation.check_out > check_in
        )

        if exclude_id is not None:
            query = query.filter(
                HotelReservation.id != exclude_id
            )

        return query.first()

    @staticmethod
    def update(
        db: Session,
        reservation: HotelReservation
    ):
        db.commit()
        db.refresh(reservation)

        return reservation

    @staticmethod
    def delete(
        db: Session,
        reservation: HotelReservation
    ):
        db.delete(reservation)
        db.commit()