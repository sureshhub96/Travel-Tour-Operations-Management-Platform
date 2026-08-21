from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.booking import Booking
from app.models.customer import Customer
from app.models.package import TourPackage

from app.repositories.booking_repository import BookingRepository


class BookingService:

    @staticmethod
    def create(
        db: Session,
        data
    ):
        customer = (
            db.query(Customer)
            .filter(Customer.id == data.customer_id)
            .first()
        )

        if not customer:
            raise HTTPException(
                status_code=404,
                detail="Customer not found"
            )

        package = (
            db.query(TourPackage)
            .filter(TourPackage.id == data.package_id)
            .first()
        )

        if not package:
            raise HTTPException(
                status_code=404,
                detail="Package not found"
            )

        if package.status == "Cancelled":
            raise HTTPException(
                status_code=400,
                detail="Cancelled package cannot accept bookings"
            )

        if package.status in ["Completed", "Full"]:
            raise HTTPException(
                status_code=400,
                detail="Package is not available for booking"
            )

        if data.number_of_travelers <= 0:
            raise HTTPException(
                status_code=400,
                detail="Number of travelers must be greater than 0"
            )

        if data.number_of_travelers > package.available_slots:
            raise HTTPException(
                status_code=400,
                detail=f"Only {package.available_slots} slots are available"
            )

        if data.booking_date > package.start_date:
            raise HTTPException(
                status_code=400,
                detail="Booking date cannot be after package start date"
            )

        base_amount = (
            package.base_price
            * data.number_of_travelers
        )

        discount = data.discount or 0
        tax = data.tax or 0

        total_amount = (
            base_amount
            + tax
            - discount
        )

        if total_amount < 0:
            raise HTTPException(
                status_code=400,
                detail="Total amount cannot be negative"
            )

        booking = Booking(
            customer_id=data.customer_id,
            package_id=data.package_id,
            booking_date=data.booking_date,
            number_of_travelers=data.number_of_travelers,
            base_amount=base_amount,
            discount=discount,
            tax=tax,
            total_amount=total_amount,
            booking_status="Pending"
        )

        package.available_slots -= data.number_of_travelers

        if package.available_slots <= 0:
            package.available_slots = 0
            package.status = "Full"

        db.add(booking)
        db.commit()
        db.refresh(booking)

        return booking

    @staticmethod
    def get(
        db: Session,
        booking_id: int
    ):
        booking = BookingRepository.get_by_id(
            db,
            booking_id
        )

        if not booking:
            raise HTTPException(
                status_code=404,
                detail="Booking not found"
            )

        return booking

    @staticmethod
    def get_all(
        db: Session
    ):
        return BookingRepository.get_all(db)

    @staticmethod
    def confirm(
        db: Session,
        booking_id: int
    ):
        booking = BookingService.get(
            db,
            booking_id
        )

        if booking.booking_status == "Cancelled":
            raise HTTPException(
                status_code=400,
                detail="Cancelled booking cannot be confirmed"
            )

        if booking.booking_status == "Completed":
            raise HTTPException(
                status_code=400,
                detail="Booking is already completed"
            )

        if booking.booking_status == "Confirmed":
            return booking

        booking.booking_status = "Confirmed"

        db.commit()
        db.refresh(booking)

        return booking

    @staticmethod
    def cancel(
        db: Session,
        booking_id: int
    ):
        booking = BookingService.get(
            db,
            booking_id
        )

        if booking.booking_status == "Cancelled":
            raise HTTPException(
                status_code=400,
                detail="Booking is already cancelled"
            )

        if booking.booking_status == "Completed":
            raise HTTPException(
                status_code=400,
                detail="Completed booking cannot be cancelled"
            )

        booking.booking_status = "Cancelled"

        package = (
            db.query(TourPackage)
            .filter(
                TourPackage.id == booking.package_id
            )
            .first()
        )

        if package:
            package.available_slots += (
                booking.number_of_travelers
            )

            if package.available_slots > package.max_capacity:
                package.available_slots = package.max_capacity

            if package.status == "Full":
                package.status = "Published"

        db.commit()
        db.refresh(booking)

        return booking