from sqlalchemy import Column, Integer, String, Text

from app.database import Base


class Destination(Base):
    __tablename__ = "destinations"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(
        String(150),
        nullable=False,
        index=True
    )

    country = Column(
        String(100),
        nullable=False,
        index=True
    )

    state = Column(
        String(100),
        nullable=True
    )

    description = Column(
        Text,
        nullable=True
    )

    best_season = Column(
        String(100),
        nullable=True
    )

    status = Column(
        String(50),
        default="Active",
        nullable=False
    )