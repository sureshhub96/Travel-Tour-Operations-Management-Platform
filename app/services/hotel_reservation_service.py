from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.booking import Booking
from app.models.hotel_reservation import HotelReservation
from app.models.room import Room


class HotelReservationService:

    # ==================================================
    # CREATE HOTEL RESERVATION
    # ==================================================

    @staticmethod
    def create(
        db: Session,
        data
    ):
        # Check booking
        booking = db.query(Booking).filter(
            Booking.id == data.booking_id
        ).first()

        if not booking:
            raise HTTPException(
                status_code=404,
                detail="Booking not found"
            )

        if booking.booking_status == "Cancelled":
            raise HTTPException(
                status_code=400,
                detail="Cannot reserve hotel for cancelled booking"
            )

        # Check room
        room = db.query(Room).filter(
            Room.id == data.room_id
        ).first()

        if not room:
            raise HTTPException(
                status_code=404,
                detail="Room not found"
            )

        if room.availability_status != "Available":
            raise HTTPException(
                status_code=400,
                detail="Room is not available"
            )

        # Validate number of rooms
        if data.number_of_rooms < 1:
            raise HTTPException(
                status_code=400,
                detail="Number of rooms must be at least 1"
            )

        # Validate dates
        if data.check_out <= data.check_in:
            raise HTTPException(
                status_code=400,
                detail="Check-out date must be after check-in date"
            )

        # Check capacity
        total_capacity = (
            room.capacity *
            data.number_of_rooms
        )

        if total_capacity < booking.number_of_travelers:
            raise HTTPException(
                status_code=400,
                detail="Room capacity is not sufficient for all travelers"
            )

        # Check overlapping reservation
        overlapping = db.query(
            HotelReservation
        ).filter(
            HotelReservation.room_id == data.room_id,
            HotelReservation.check_in < data.check_out,
            HotelReservation.check_out > data.check_in
        ).first()

        if overlapping:
            raise HTTPException(
                status_code=400,
                detail="Room is already reserved for the selected dates"
            )

        # Calculate nights
        nights = (
            data.check_out -
            data.check_in
        ).days

        # Calculate total amount
        total_amount = (
            room.price_per_night
            * data.number_of_rooms
            * nights
        )

        # Create reservation
        reservation = HotelReservation(
            booking_id=data.booking_id,
            room_id=data.room_id,
            check_in=data.check_in,
            check_out=data.check_out,
            number_of_rooms=data.number_of_rooms,
            total_amount=total_amount
        )

        db.add(reservation)
        db.commit()
        db.refresh(reservation)

        return reservation

    # ==================================================
    # GET ALL HOTEL RESERVATIONS
    # ==================================================

    @staticmethod
    def get_all(
        db: Session,
        booking_id: int | None = None,
        room_id: int | None = None,
        page: int = 1,
        limit: int = 10
    ):
        query = db.query(HotelReservation)

        if booking_id is not None:
            query = query.filter(
                HotelReservation.booking_id == booking_id
            )

        if room_id is not None:
            query = query.filter(
                HotelReservation.room_id == room_id
            )

        offset = (page - 1) * limit

        return (
            query
            .offset(offset)
            .limit(limit)
            .all()
        )

    # ==================================================
    # GET RESERVATION BY ID
    # ==================================================

    @staticmethod
    def get(
        db: Session,
        reservation_id: int
    ):
        reservation = db.query(
            HotelReservation
        ).filter(
            HotelReservation.id == reservation_id
        ).first()

        if not reservation:
            raise HTTPException(
                status_code=404,
                detail="Hotel reservation not found"
            )

        return reservation

    # ==================================================
    # CANCEL HOTEL RESERVATION
    # ==================================================

    @staticmethod
    def cancel(
        db: Session,
        reservation_id: int
    ):
        reservation = db.query(
            HotelReservation
        ).filter(
            HotelReservation.id == reservation_id
        ).first()

        if not reservation:
            raise HTTPException(
                status_code=404,
                detail="Hotel reservation not found"
            )

        # Check whether status field exists in your model
        if hasattr(reservation, "status"):
            if reservation.status == "Cancelled":
                raise HTTPException(
                    status_code=400,
                    detail="Hotel reservation is already cancelled"
                )

            reservation.status = "Cancelled"

        elif hasattr(reservation, "reservation_status"):
            if reservation.reservation_status == "Cancelled":
                raise HTTPException(
                    status_code=400,
                    detail="Hotel reservation is already cancelled"
                )

            reservation.reservation_status = "Cancelled"

        else:
            raise HTTPException(
                status_code=500,
                detail="Reservation status field is missing in HotelReservation model"
            )

        db.commit()
        db.refresh(reservation)

        return reservation