from datetime import date

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.booking import Booking
from app.models.cancellation import Cancellation
from app.models.package import TourPackage
from app.models.payment import Payment


class CancellationService:

    @staticmethod
    def calculate_refund(
        tour_start_date,
        paid_amount
    ):

        today = date.today()

        days_remaining = (
            tour_start_date - today
        ).days

        if days_remaining >= 15:
            refund_percentage = 0.90

        elif days_remaining >= 7:
            refund_percentage = 0.70

        elif days_remaining >= 2:
            refund_percentage = 0.40

        else:
            refund_percentage = 0.0

        return round(
            paid_amount * refund_percentage,
            2
        )

    @staticmethod
    def cancel_booking(
        db: Session,
        booking_id: int,
        data
    ):

        # --------------------------------
        # Find booking
        # --------------------------------

        booking = db.query(Booking).filter(
            Booking.id == booking_id
        ).first()

        if not booking:

            raise HTTPException(
                status_code=404,
                detail="Booking not found"
            )

        # --------------------------------
        # Prevent duplicate cancellation
        # --------------------------------

        if booking.booking_status == "Cancelled":

            raise HTTPException(
                status_code=400,
                detail="Booking is already cancelled"
            )

        # --------------------------------
        # Find package
        # --------------------------------

        package = db.query(TourPackage).filter(
            TourPackage.id == booking.package_id
        ).first()

        if not package:

            raise HTTPException(
                status_code=404,
                detail="Package not found"
            )

        # --------------------------------
        # Calculate paid amount
        # --------------------------------

        successful_payments = db.query(Payment).filter(
            Payment.booking_id == booking_id,
            Payment.payment_status == "Success"
        ).all()

        paid_amount = sum(
            payment.amount
            for payment in successful_payments
        )

        # --------------------------------
        # Calculate refund
        # --------------------------------

        refund_amount = CancellationService.calculate_refund(
            package.start_date,
            paid_amount
        )

        # --------------------------------
        # Update booking
        # --------------------------------

        booking.booking_status = "Cancelled"

        # --------------------------------
        # Restore package slots
        # --------------------------------

        if booking.booking_status == "Cancelled":

            package.available_slots += (
                booking.number_of_travelers
            )

            if package.status == "Full":

                package.status = "Published"

        # --------------------------------
        # Create cancellation history
        # --------------------------------

        cancellation = Cancellation(
            booking_id=booking_id,
            cancellation_reason=data.reason,
            refund_amount=refund_amount
        )

        db.add(cancellation)

        # --------------------------------
        # Mark payment as refunded
        # --------------------------------

        if refund_amount > 0:

            remaining_refund = refund_amount

            for payment in successful_payments:

                if remaining_refund <= 0:
                    break

                payment_refund = min(
                    payment.amount,
                    remaining_refund
                )

                if payment_refund == payment.amount:
                    payment.payment_status = "Refunded"

                remaining_refund -= payment_refund

        db.commit()

        db.refresh(cancellation)

        return cancellation

    @staticmethod
    def get_all(
        db: Session
    ):

        return db.query(
            Cancellation
        ).all()