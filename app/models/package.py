from sqlalchemy import (
    Column,
    Date,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)

from app.database import Base


class TourPackage(Base):

    __tablename__ = "tour_packages"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    package_name = Column(
        String(200),
        nullable=False
    )

    destination_id = Column(
        Integer,
        ForeignKey("destinations.id"),
        nullable=False
    )

    description = Column(
        Text,
        nullable=True
    )

    duration_days = Column(
        Integer,
        nullable=False
    )

    base_price = Column(
        Float,
        nullable=False
    )

    max_capacity = Column(
        Integer,
        nullable=False
    )

    available_slots = Column(
        Integer,
        nullable=False
    )

    start_date = Column(
        Date,
        nullable=False
    )

    end_date = Column(
        Date,
        nullable=False
    )

    status = Column(
        String(50),
        default="Draft",
        nullable=False
    )

    guide_id = Column(
        Integer,
        ForeignKey("guides.id"),
        nullable=True,
        index=True
    )