from sqlalchemy.orm import Session

from app.models.hotel import Hotel


class HotelRepository:

    # ==================================================
    # CREATE HOTEL
    # ==================================================

    @staticmethod
    def create(
        db: Session,
        hotel: Hotel
    ):
        db.add(hotel)
        db.commit()
        db.refresh(hotel)

        return hotel

    # ==================================================
    # GET HOTEL BY ID
    # ==================================================

    @staticmethod
    def get_by_id(
        db: Session,
        hotel_id: int
    ):
        return db.query(Hotel).filter(
            Hotel.id == hotel_id
        ).first()

    # ==================================================
    # GET ALL HOTELS
    # ==================================================

    @staticmethod
    def get_all(
        db: Session,
        destination_id: int | None = None,
        min_rating: float | None = None,
        page: int = 1,
        limit: int = 10
    ):

        query = db.query(Hotel)

        # Destination filter
        if destination_id is not None:
            query = query.filter(
                Hotel.destination_id == destination_id
            )

        # Rating filter
        if min_rating is not None:
            query = query.filter(
                Hotel.rating >= min_rating
            )

        # Pagination
        return (
            query
            .offset((page - 1) * limit)
            .limit(limit)
            .all()
        )

    # ==================================================
    # GET HOTELS BY DESTINATION
    # ==================================================

    @staticmethod
    def get_by_destination(
        db: Session,
        destination_id: int
    ):
        return db.query(Hotel).filter(
            Hotel.destination_id == destination_id
        ).all()

    # ==================================================
    # CHECK HOTEL NAME
    # ==================================================

    @staticmethod
    def get_by_name(
        db: Session,
        hotel_name: str
    ):
        return db.query(Hotel).filter(
            Hotel.hotel_name == hotel_name
        ).first()

    # ==================================================
    # UPDATE HOTEL
    # ==================================================

    @staticmethod
    def update(
        db: Session,
        hotel: Hotel
    ):
        db.commit()
        db.refresh(hotel)

        return hotel

    # ==================================================
    # DELETE HOTEL
    # ==================================================

    @staticmethod
    def delete(
        db: Session,
        hotel: Hotel
    ):
        db.delete(hotel)
        db.commit()

        return True