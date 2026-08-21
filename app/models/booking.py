from sqlalchemy import (
    Column,
    Date,
    Float,
    ForeignKey,
    Integer,
    String,
)

from app.database import Base


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    customer_id = Column(
        Integer,
        ForeignKey("customers.id"),
        nullable=False,
        index=True
    )

    package_id = Column(
        Integer,
        ForeignKey("tour_packages.id"),
        nullable=False,
        index=True
    )

    booking_date = Column(
        Date,
        nullable=False
    )

    number_of_travelers = Column(
        Integer,
        nullable=False
    )

    base_amount = Column(
        Float,
        nullable=False
    )

    discount = Column(
        Float,
        default=0
    )

    tax = Column(
        Float,
        default=0
    )

    total_amount = Column(
        Float,
        nullable=False
    )

    booking_status = Column(
        String(50),
        default="Pending",
        nullable=False
    )