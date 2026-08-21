from sqlalchemy import Column, Integer, String, Float, ForeignKey

from app.database import Base


class Hotel(Base):
    __tablename__ = "hotels"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    hotel_name = Column(
        String(200),
        nullable=False
    )

    destination_id = Column(
        Integer,
        ForeignKey("destinations.id"),
        nullable=False,
        index=True
    )

    address = Column(
        String(500),
        nullable=True
    )

    rating = Column(
        Float,
        nullable=True
    )

    contact_number = Column(
        String(20),
        nullable=True
    )