from datetime import datetime


class NotificationService:

    @staticmethod
    def send_booking_confirmation(
        customer_email: str,
        booking_id: int
    ):
        print(
            f"[NOTIFICATION] Booking confirmation sent "
            f"to {customer_email} for booking #{booking_id}"
        )

    @staticmethod
    def send_payment_success(
        customer_email: str,
        booking_id: int,
        amount: float
    ):
        print(
            f"[NOTIFICATION] Payment success sent "
            f"to {customer_email} for booking #{booking_id}. "
            f"Amount: {amount}"
        )

    @staticmethod
    def send_payment_failure(
        customer_email: str,
        booking_id: int
    ):
        print(
            f"[NOTIFICATION] Payment failure sent "
            f"to {customer_email} for booking #{booking_id}"
        )

    @staticmethod
    def send_booking_cancellation(
        customer_email: str,
        booking_id: int
    ):
        print(
            f"[NOTIFICATION] Cancellation notification sent "
            f"to {customer_email} for booking #{booking_id}"
        )

    @staticmethod
    def send_refund_notification(
        customer_email: str,
        booking_id: int,
        refund_amount: float
    ):
        print(
            f"[NOTIFICATION] Refund notification sent "
            f"to {customer_email} for booking #{booking_id}. "
            f"Refund: {refund_amount}"
        )

    @staticmethod
    def send_hotel_confirmation(
        customer_email: str,
        reservation_id: int
    ):
        print(
            f"[NOTIFICATION] Hotel reservation confirmation "
            f"sent to {customer_email} "
            f"for reservation #{reservation_id}"
        )

    @staticmethod
    def send_upcoming_tour_reminder(
        customer_email: str,
        package_name: str,
        start_date
    ):
        print(
            f"[NOTIFICATION] Upcoming tour reminder sent "
            f"to {customer_email}. "
            f"Package: {package_name}, "
            f"Start date: {start_date}"
        )