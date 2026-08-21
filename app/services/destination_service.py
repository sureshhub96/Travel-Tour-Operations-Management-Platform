from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.destination import Destination
from app.repositories.destination_repository import DestinationRepository


class DestinationService:

    @staticmethod
    def create(db: Session, data):
        destination = Destination(**data.model_dump())
        return DestinationRepository.create(db, destination)

    @staticmethod
    def get(db: Session, destination_id: int):
        destination = DestinationRepository.get_by_id(db, destination_id)

        if not destination:
            raise HTTPException(404, "Destination not found")

        return destination

    @staticmethod
    def update(db: Session, destination_id: int, data):
        destination = DestinationService.get(db, destination_id)

        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(destination, key, value)

        db.commit()
        db.refresh(destination)

        return destination

    @staticmethod
    def delete(db: Session, destination_id: int):
        destination = DestinationService.get(db, destination_id)
        DestinationRepository.delete(db, destination)