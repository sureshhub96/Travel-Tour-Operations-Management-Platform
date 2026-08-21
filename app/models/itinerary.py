from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    Text,
    Time,
    UniqueConstraint,
)

from app.database import Base


class Itinerary(Base):
    __tablename__ = "itineraries"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    package_id = Column(
        Integer,
        ForeignKey("tour_packages.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    day_number = Column(
        Integer,
        nullable=False
    )

    title = Column(
        String(200),
        nullable=False
    )

    description = Column(
        Text,
        nullable=True
    )

    location = Column(
        String(200),
        nullable=True
    )

    start_time = Column(
        Time,
        nullable=False
    )

    end_time = Column(
        Time,
        nullable=False
    )

    __table_args__ = (
        UniqueConstraint(
            "package_id",
            "day_number",
            name="uq_package_day"
        ),
    )