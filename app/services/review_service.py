from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.booking import Booking
from app.models.customer import Customer
from app.models.package import TourPackage
from app.models.review import Review


class ReviewService:

    # -----------------------------------------
    # Create Review
    # -----------------------------------------

    @staticmethod
    def create(
        db: Session,
        customer_id: int,
        data
    ):

        # Check customer
        customer = db.query(Customer).filter(
            Customer.id == customer_id
        ).first()

        if not customer:

            raise HTTPException(
                status_code=404,
                detail="Customer not found"
            )

        # Check package
        package = db.query(TourPackage).filter(
            TourPackage.id == data.package_id
        ).first()

        if not package:

            raise HTTPException(
                status_code=404,
                detail="Package not found"
            )

        # Check booking
        booking = db.query(Booking).filter(
            Booking.id == data.booking_id
        ).first()

        if not booking:

            raise HTTPException(
                status_code=404,
                detail="Booking not found"
            )

        # Booking must belong to customer
        if booking.customer_id != customer_id:

            raise HTTPException(
                status_code=403,
                detail="You can review only your own booking"
            )

        # Booking must belong to package
        if booking.package_id != data.package_id:

            raise HTTPException(
                status_code=400,
                detail="Booking does not belong to this package"
            )

        # Booking must be completed
        if booking.booking_status != "Completed":

            raise HTTPException(
                status_code=400,
                detail="Only completed bookings can be reviewed"
            )

        # Check duplicate review
        existing_review = db.query(Review).filter(
            Review.booking_id == data.booking_id
        ).first()

        if existing_review:

            raise HTTPException(
                status_code=400,
                detail="This booking has already been reviewed"
            )

        # Create review
        review = Review(
            customer_id=customer_id,
            package_id=data.package_id,
            booking_id=data.booking_id,
            rating=data.rating,
            review_text=data.review_text
        )

        db.add(review)
        db.commit()
        db.refresh(review)

        return review

    # -----------------------------------------
    # Get Package Reviews
    # -----------------------------------------

    @staticmethod
    def get_package_reviews(
        db: Session,
        package_id: int
    ):

        package = db.query(TourPackage).filter(
            TourPackage.id == package_id
        ).first()

        if not package:

            raise HTTPException(
                status_code=404,
                detail="Package not found"
            )

        return db.query(Review).filter(
            Review.package_id == package_id
        ).all()

    # -----------------------------------------
    # Update Review
    # -----------------------------------------

    @staticmethod
    def update(
        db: Session,
        review_id: int,
        customer_id: int,
        data
    ):

        review = db.query(Review).filter(
            Review.id == review_id
        ).first()

        if not review:

            raise HTTPException(
                status_code=404,
                detail="Review not found"
            )

        # Only owner can update
        if review.customer_id != customer_id:

            raise HTTPException(
                status_code=403,
                detail="You can update only your own review"
            )

        if data.rating is not None:

            review.rating = data.rating

        if data.review_text is not None:

            review.review_text = data.review_text

        db.commit()
        db.refresh(review)

        return review

    # -----------------------------------------
    # Delete Review
    # -----------------------------------------

    @staticmethod
    def delete(
        db: Session,
        review_id: int,
        customer_id: int
    ):

        review = db.query(Review).filter(
            Review.id == review_id
        ).first()

        if not review:

            raise HTTPException(
                status_code=404,
                detail="Review not found"
            )

        # Only owner can delete
        if review.customer_id != customer_id:

            raise HTTPException(
                status_code=403,
                detail="You can delete only your own review"
            )

        db.delete(review)
        db.commit()

        return {
            "message": "Review deleted successfully"
        }