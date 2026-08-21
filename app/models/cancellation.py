from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from datetime import datetime

from app.database import Base


class Cancellation(Base):
    __tablename__ = "cancellations"

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

    cancellation_reason = Column(
        String(500),
        nullable=False
    )

    refund_amount = Column(
        Float,
        default=0,
        nullable=False
    )

    cancellation_date = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )