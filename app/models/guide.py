from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    String,
    Text,
)

from app.database import Base


class Guide(Base):

    __tablename__ = "guides"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String(100),
        nullable=False
    )

    email = Column(
        String(150),
        nullable=True
    )

    phone = Column(
        String(20),
        nullable=True
    )

    language = Column(
        String(100),
        nullable=True
    )

    specialization = Column(
        String(200),
        nullable=True
    )

    experience_years = Column(
        Integer,
        default=0
    )

    bio = Column(
        Text,
        nullable=True
    )

    is_available = Column(
        Boolean,
        default=True
    )