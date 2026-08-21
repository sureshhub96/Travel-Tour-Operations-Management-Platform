from sqlalchemy import Column, Integer, String

from app.database import Base


class Customer(Base):
    __tablename__ = "customers"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String(150),
        nullable=False
    )

    email = Column(
        String(255),
        unique=True,
        nullable=False,
        index=True
    )

    phone = Column(
        String(20),
        nullable=True
    )

    address = Column(
        String(500),
        nullable=True
    )

    emergency_contact = Column(
        String(100),
        nullable=True
    )