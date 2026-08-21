from sqlalchemy.orm import Session

from app.models.room import Room


class RoomRepository:

    @staticmethod
    def create(
        db: Session,
        room: Room
    ):
        db.add(room)
        db.commit()
        db.refresh(room)

        return room

    @staticmethod
    def get_by_id(
        db: Session,
        room_id: int
    ):
        return db.query(Room).filter(
            Room.id == room_id
        ).first()

    @staticmethod
    def get_all(
        db: Session,
        hotel_id: int | None = None,
        room_type: str | None = None,
        availability_status: str | None = None,
        page: int = 1,
        limit: int = 10
    ):

        query = db.query(Room)

        if hotel_id is not None:
            query = query.filter(
                Room.hotel_id == hotel_id
            )

        if room_type:
            query = query.filter(
                Room.room_type == room_type
            )

        if availability_status:
            query = query.filter(
                Room.availability_status ==
                availability_status
            )

        return (
            query
            .offset((page - 1) * limit)
            .limit(limit)
            .all()
        )

    @staticmethod
    def get_by_hotel(
        db: Session,
        hotel_id: int
    ):
        return db.query(Room).filter(
            Room.hotel_id == hotel_id
        ).all()

    @staticmethod
    def update(
        db: Session,
        room: Room
    ):
        db.commit()
        db.refresh(room)

        return room

    @staticmethod
    def delete(
        db: Session,
        room: Room
    ):
        db.delete(room)
        db.commit()