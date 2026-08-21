from sqlalchemy.orm import Session
from app.models.destination import Destination


class DestinationRepository:

    @staticmethod
    def create(db: Session, destination: Destination):
        db.add(destination)
        db.commit()
        db.refresh(destination)
        return destination

    @staticmethod
    def get_all(db: Session):
        return db.query(Destination).all()

    @staticmethod
    def get_by_id(db: Session, destination_id: int):
        return db.query(Destination).filter(
            Destination.id == destination_id
        ).first()

    @staticmethod
    def delete(db: Session, destination):
        db.delete(destination)
        db.commit()