from sqlalchemy.orm import Session

from app.models.review import Review


class ReviewRepository:

    @staticmethod
    def create(
        db: Session,
        review: Review
    ):
        db.add(review)
        db.commit()
        db.refresh(review)

        return review

    @staticmethod
    def get_by_id(
        db: Session,
        review_id: int
    ):
        return db.query(Review).filter(
            Review.id == review_id
        ).first()

    @staticmethod
    def get_all(
        db: Session
    ):
        return db.query(Review).all()

    @staticmethod
    def get_by_package(
        db: Session,
        package_id: int
    ):
        return db.query(Review).filter(
            Review.package_id == package_id
        ).all()

    @staticmethod
    def get_by_customer(
        db: Session,
        customer_id: int
    ):
        return db.query(Review).filter(
            Review.customer_id == customer_id
        ).all()

    @staticmethod
    def get_by_booking(
        db: Session,
        booking_id: int
    ):
        return db.query(Review).filter(
            Review.booking_id == booking_id
        ).first()

    @staticmethod
    def update(
        db: Session,
        review: Review
    ):
        db.commit()
        db.refresh(review)

        return review

    @staticmethod
    def delete(
        db: Session,
        review: Review
    ):
        db.delete(review)
        db.commit()