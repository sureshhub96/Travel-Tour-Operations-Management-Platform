from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from datetime import datetime

from app.database import Base


class Payment(Base):
    __tablename__ = "payments"

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

    amount = Column(
        Float,
        nullable=False
    )

    payment_method = Column(
        String(50),
        nullable=False
    )

    transaction_id = Column(
        String(200),
        unique=True,
        nullable=False,
        index=True
    )

    payment_status = Column(
        String(50),
        default="Pending",
        nullable=False
    )

    payment_date = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )