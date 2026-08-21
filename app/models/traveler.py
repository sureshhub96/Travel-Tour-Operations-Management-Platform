from sqlalchemy import Column, Date, ForeignKey, Integer, String, Text

from app.database import Base


class Traveler(Base):
    __tablename__ = "travelers"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    booking_id = Column(
        Integer,
        ForeignKey("bookings.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    full_name = Column(
        String(150),
        nullable=False
    )

    date_of_birth = Column(
        Date,
        nullable=False
    )

    gender = Column(
        String(20),
        nullable=False
    )

    passport_number = Column(
        String(50),
        unique=True,
        nullable=True,
        index=True
    )

    nationality = Column(
        String(100),
        nullable=False
    )

    special_requirements = Column(
        Text,
        nullable=True
    )