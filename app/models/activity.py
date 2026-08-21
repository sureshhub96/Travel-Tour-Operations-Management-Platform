from sqlalchemy import Column, Integer, String, Float, ForeignKey

from app.database import Base


class Activity(Base):
    __tablename__ = "activities"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    package_id = Column(
        Integer,
        ForeignKey("tour_packages.id"),
        nullable=False,
        index=True
    )

    activity_name = Column(
        String(200),
        nullable=False
    )

    location = Column(
        String(200),
        nullable=False
    )

    duration = Column(
        Integer,
        nullable=False
    )

    price = Column(
        Float,
        nullable=False
    )

    capacity = Column(
        Integer,
        nullable=False
    )