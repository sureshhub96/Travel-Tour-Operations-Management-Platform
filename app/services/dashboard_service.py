from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.models.package import TourPackage
from app.models.booking import Booking
from app.models.payment import Payment


class DashboardService:

    # ==================================================
    # DASHBOARD SUMMARY
    # ==================================================

    @staticmethod
    def get_summary(db: Session):

        total_customers = (
            db.queryfunc.count(Customer.id)
            .scalar()
            or 0
        )

        total_packages = (
            db.queryfunc.count(TourPackage.id)
            .scalar()
            or 0
        )

        active_tours = (
    db.query(
        func.count(TourPackage.id)
    )
    .filter(
        TourPackage.status == "Published"
    )
    .scalar()
    or 0
)

        total_bookings = (
    db.query(
        func.count(Booking.id)
    )
    .scalar()
    or 0
)


        confirmed_bookings = (
    db.query(
        func.count(Booking.id)
    )
    .filter(
        Booking.booking_status == "Confirmed"
    )
    .scalar()
    or 0
)

        cancelled_bookings = (
    db.query(
        func.count(Booking.id)
    )
    .filter(
        Booking.booking_status == "Cancelled"
    )
    .scalar()
    or 0
)

        total_revenue = (
            db.query(
                func.coalesce(
                    func.sum(Payment.amount),
                    0
                )
            )
            .filter(
                Payment.payment_status == "Success"
            )
            .scalar()
            or 0
        )

        total_refunds = (
            db.query(
                func.coalesce(
                    func.sum(Payment.amount),
                    0
                )
            )
            .filter(
                Payment.payment_status == "Refunded"
            )
            .scalar()
            or 0
        )

        return {
            "total_customers": total_customers,
            "total_packages": total_packages,
            "active_tours": active_tours,
            "total_bookings": total_bookings,
            "confirmed_bookings": confirmed_bookings,
            "cancelled_bookings": cancelled_bookings,
            "total_revenue": float(total_revenue),
            "total_refunds": float(total_refunds),
        }

    # ==================================================
    # REVENUE
    # ==================================================

    @staticmethod
    def get_revenue(db: Session):

        total_revenue = (
            db.query(
                func.coalesce(
                    func.sum(Payment.amount),
                    0
                )
            )
            .filter(
                Payment.payment_status == "Success"
            )
            .scalar()
            or 0
        )

        total_refunds = (
            db.query(
                func.coalesce(
                    func.sum(Payment.amount),
                    0
                )
            )
            .filter(
                Payment.payment_status == "Refunded"
            )
            .scalar()
            or 0
        )

        net_revenue = (
            float(total_revenue)
            - float(total_refunds)
        )

        return {
            "total_revenue": float(total_revenue),
            "total_refunds": float(total_refunds),
            "net_revenue": net_revenue,
        }

    # ==================================================
    # BOOKING STATISTICS
    # ==================================================

    @staticmethod
    def get_bookings(db: Session):

        total = (
    db.query(
        func.count(Booking.id)
    )
    .scalar()
    or 0
)

        pending = (
    db.query(
        func.count(Booking.id)
    )
    .filter(
        Booking.booking_status == "Pending"
    )
    .scalar()
    or 0
)
        confirmed = (
    db.query(
        func.count(Booking.id)
    )
    .filter(
        Booking.booking_status == "Confirmed"
    )
    .scalar()
    or 0
)

       cancelled = (
    db.query(
        func.count(Booking.id)
    )
    .filter(
        Booking.booking_status == "Cancelled"
    )
    .scalar()
    or 0
)

    completed = (
    db.query(
        func.count(Booking.id)
    )
    .filter(
        Booking.booking_status == "Completed"
    )
    .scalar()
    or 0
)

       return {
    "total_bookings": total,
    "pending_bookings": pending,
    "confirmed_bookings": confirmed,
    "cancelled_bookings": cancelled,
    "completed_bookings": completed,
}