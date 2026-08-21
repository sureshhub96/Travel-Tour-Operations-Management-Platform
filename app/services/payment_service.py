from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.booking import Booking
from app.models.package import TourPackage
from app.models.payment import Payment


class PaymentService:

    VALID_METHODS = {
        "UPI",
        "Card",
        "Net Banking",
        "Wallet"
    }

    @staticmethod
    def create_payment(
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
        # Check cancelled booking
        # --------------------------------

        if booking.booking_status == "Cancelled":

            raise HTTPException(
                status_code=400,
                detail="Cannot make payment for cancelled booking"
            )

        # --------------------------------
        # Validate payment method
        # --------------------------------

        if data.payment_method not in PaymentService.VALID_METHODS:

            raise HTTPException(
                status_code=400,
                detail=(
                    "Invalid payment method. "
                    "Use UPI, Card, Net Banking or Wallet"
                )
            )

        # --------------------------------
        # Prevent duplicate transaction
        # --------------------------------

        existing_transaction = db.query(Payment).filter(
            Payment.transaction_id == data.transaction_id
        ).first()

        if existing_transaction:

            raise HTTPException(
                status_code=400,
                detail="Transaction ID already exists"
            )

        # --------------------------------
        # Check payment amount
        # --------------------------------

        if data.amount > booking.total_amount:

            raise HTTPException(
                status_code=400,
                detail="Payment cannot exceed booking amount"
            )

        # --------------------------------
        # Check previous successful payments
        # --------------------------------

        paid_amount = db.query(Payment).filter(
            Payment.booking_id == booking_id,
            Payment.payment_status == "Success"
        ).all()

        total_paid = sum(
            payment.amount
            for payment in paid_amount
        )

        if total_paid + data.amount > booking.total_amount:

            raise HTTPException(
                status_code=400,
                detail="Total payment cannot exceed booking amount"
            )

        # --------------------------------
        # Create payment
        # --------------------------------

        payment = Payment(
            booking_id=booking_id,
            amount=data.amount,
            payment_method=data.payment_method,
            transaction_id=data.transaction_id,
            payment_status="Success"
        )

        db.add(payment)

        # --------------------------------
        # Confirm booking if fully paid
        # --------------------------------

        new_total_paid = total_paid + data.amount

        if new_total_paid >= booking.total_amount:

            if booking.booking_status == "Pending":

                package = db.query(TourPackage).filter(
                    TourPackage.id == booking.package_id
                ).first()

                if not package:

                    raise HTTPException(
                        status_code=404,
                        detail="Package not found"
                    )

                if package.available_slots < booking.number_of_travelers:

                    raise HTTPException(
                        status_code=400,
                        detail="Not enough package slots available"
                    )

                # Reduce slots only after successful confirmation
                package.available_slots -= (
                    booking.number_of_travelers
                )

                # Update package status
                if package.available_slots == 0:
                    package.status = "Full"

                booking.booking_status = "Confirmed"

        db.commit()

        db.refresh(payment)

        return payment

    @staticmethod
    def get_all(
        db: Session
    ):

        return db.query(Payment).all()

    @staticmethod
    def get_by_id(
        db: Session,
        payment_id: int
    ):

        payment = db.query(Payment).filter(
            Payment.id == payment_id
        ).first()

        if not payment:

            raise HTTPException(
                status_code=404,
                detail="Payment not found"
            )

        return payment

    @staticmethod
    def refund(
        db: Session,
        payment_id: int
    ):

        payment = db.query(Payment).filter(
            Payment.id == payment_id
        ).first()

        if not payment:

            raise HTTPException(
                status_code=404,
                detail="Payment not found"
            )

        if payment.payment_status != "Success":

            raise HTTPException(
                status_code=400,
                detail="Only successful payments can be refunded"
            )

        payment.payment_status = "Refunded"

        db.commit()
        db.refresh(payment)

        return payment