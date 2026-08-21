from datetime import date, datetime
from calendar import monthrange

from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.booking import Booking
from app.models.customer import Customer
from app.models.destination import Destination
from app.models.package import TourPackage
from app.models.payment import Payment


class ReportService:

    # ==================================================
    # DAILY BOOKING REPORT
    # ==================================================

    @staticmethod
    def daily_booking_report(
        db: Session,
        report_date: date | None = None
    ):

        if report_date is None:
            report_date = date.today()

        bookings = db.query(Booking).filter(
            Booking.booking_date == report_date
        ).all()

        return {
            "date": report_date,
            "total_bookings": len(bookings),
            "pending_bookings": sum(
                1 for b in bookings
                if b.booking_status == "Pending"
            ),
            "confirmed_bookings": sum(
                1 for b in bookings
                if b.booking_status == "Confirmed"
            ),
            "cancelled_bookings": sum(
                1 for b in bookings
                if b.booking_status == "Cancelled"
            ),
            "completed_bookings": sum(
                1 for b in bookings
                if b.booking_status == "Completed"
            ),
            "total_amount": sum(
                float(b.total_amount or 0)
                for b in bookings
            ),
        }

    # ==================================================
    # MONTHLY REVENUE REPORT
    # ==================================================

    @staticmethod
    def monthly_revenue_report(
        db: Session,
        year: int,
        month: int
    ):

        start_date = date(
            year,
            month,
            1
        )

        last_day = monthrange(
            year,
            month
        )[1]

        end_date = date(
            year,
            month,
            last_day
        )

        total_revenue = db.query(
            func.coalesce(
                func.sum(Payment.amount),
                0
            )
        ).filter(
            Payment.payment_status == "Success"
        ).filter(
            Payment.payment_date >= start_date
        ).filter(
            Payment.payment_date <= end_date
        ).scalar()

        total_refunds = db.query(
            func.coalesce(
                func.sum(Payment.amount),
                0
            )
        ).filter(
            Payment.payment_status == "Refunded"
        ).filter(
            Payment.payment_date >= start_date
        ).filter(
            Payment.payment_date <= end_date
        ).scalar()

        booking_count = db.query(
            func.count(Booking.id)
        ).filter(
            Booking.booking_date >= start_date
        ).filter(
            Booking.booking_date <= end_date
        ).scalar() or 0

        total_revenue = float(
            total_revenue or 0
        )

        total_refunds = float(
            total_refunds or 0
        )

        return {
            "year": year,
            "month": month,
            "total_bookings": booking_count,
            "total_revenue": total_revenue,
            "total_refunds": total_refunds,
            "net_revenue": (
                total_revenue -
                total_refunds
            ),
        }

    # ==================================================
    # DESTINATION-WISE REVENUE
    # ==================================================

    @staticmethod
    def destination_revenue_report(
        db: Session
    ):

        results = (
            db.query(
                Destination.id,
                Destination.name,
                func.count(
                    Booking.id
                ).label("total_bookings"),
                func.coalesce(
                    func.sum(
                        Booking.total_amount
                    ),
                    0
                ).label("revenue")
            )
            .join(
                TourPackage,
                TourPackage.destination_id ==
                Destination.id
            )
            .join(
                Booking,
                Booking.package_id ==
                TourPackage.id
            )
            .group_by(
                Destination.id,
                Destination.name
            )
            .order_by(
                func.sum(
                    Booking.total_amount
                ).desc()
            )
            .all()
        )

        return [
            {
                "destination_id": row.id,
                "destination_name": row.name,
                "total_bookings": row.total_bookings,
                "revenue": float(
                    row.revenue or 0
                ),
            }
            for row in results
        ]

    # ==================================================
    # PACKAGE PERFORMANCE
    # ==================================================

    @staticmethod
    def package_performance_report(
        db: Session
    ):

        results = (
            db.query(
                TourPackage.id,
                TourPackage.package_name,
                func.count(
                    Booking.id
                ).label("total_bookings"),
                func.coalesce(
                    func.sum(
                        Booking.number_of_travelers
                    ),
                    0
                ).label("total_travelers"),
                func.coalesce(
                    func.sum(
                        Booking.total_amount
                    ),
                    0
                ).label("revenue")
            )
            .outerjoin(
                Booking,
                Booking.package_id ==
                TourPackage.id
            )
            .group_by(
                TourPackage.id,
                TourPackage.package_name
            )
           .order_by(
    func.count(
        Booking.id
    ).desc()
)
            .all()
        )

        return [
            {
                "package_id": row.id,
                "package_name": row.package_name,
                "total_bookings": row.total_bookings,
                "total_travelers": row.total_travelers,
                "revenue": float(
                    row.revenue or 0
                ),
            }
            for row in results
        ]

    # ==================================================
    # CANCELLATION REPORT
    # ==================================================

    @staticmethod
    def cancellation_report(
        db: Session,
        start_date: date | None = None,
        end_date: date | None = None
    ):

        query = db.query(Booking).filter(
            Booking.booking_status == "Cancelled"
        )

        if start_date:
            query = query.filter(
                Booking.booking_date >= start_date
            )

        if end_date:
            query = query.filter(
                Booking.booking_date <= end_date
            )

        bookings = query.all()

        total_cancelled = len(bookings)

        total_amount = sum(
            float(
                booking.total_amount or 0
            )
            for booking in bookings
        )

        return {
            "start_date": start_date,
            "end_date": end_date,
            "total_cancelled_bookings":
                total_cancelled,
            "total_cancelled_amount":
                total_amount,
        }

    # ==================================================
    # CUSTOMER BOOKING HISTORY
    # ==================================================

    @staticmethod
    def customer_booking_history(
        db: Session,
        customer_id: int
    ):

        customer = db.query(
            Customer
        ).filter(
            Customer.id == customer_id
        ).first()

        if not customer:
            raise HTTPException(
                status_code=404,
                detail="Customer not found"
            )

        bookings = db.query(
            Booking
        ).filter(
            Booking.customer_id ==
            customer_id
        ).order_by(
            Booking.booking_date.desc()
        ).all()

        return {
            "customer_id": customer.id,
            "customer_name": customer.name,
            "customer_email": customer.email,
            "total_bookings": len(bookings),
            "bookings": [
                {
                    "booking_id": booking.id,
                    "package_id": booking.package_id,
                    "booking_date":
                        booking.booking_date,
                    "number_of_travelers":
                        booking.number_of_travelers,
                    "total_amount":
                        float(
                            booking.total_amount or 0
                        ),
                    "booking_status":
                        booking.booking_status,
                }
                for booking in bookings
            ],
        }