from sqlalchemy import (
    Column,
    Date,
    Float,
    ForeignKey,
    Integer,
    String,
)

from app.database import Base


class HotelReservation(Base):
    __tablename__ = "hotel_reservations"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    booking_id = Column(
        Integer,
        ForeignKey("bookings.id"),
        nullable=False,
        index=True
    )

    room_id = Column(
        Integer,
        ForeignKey("rooms.id"),
        nullable=False,
        index=True
    )

    check_in = Column(
        Date,
        nullable=False
    )

    check_out = Column(
        Date,
        nullable=False
    )

    number_of_rooms = Column(
        Integer,
        nullable=False
    )

    total_amount = Column(
        Float,
        nullable=False
    )

    status = Column(
        String(20),
        nullable=False,
        default="Confirmed"
    )