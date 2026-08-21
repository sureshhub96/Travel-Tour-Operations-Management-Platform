def payment_success_task(
    email: str,
    booking_id: int,
    amount: float,
):
    print(
        f"Payment successful | "
        f"Booking: {booking_id} | "
        f"Amount: {amount} | "
        f"Email: {email}"
    )


def payment_failure_task(
    email: str,
    booking_id: int,
):
    print(
        f"Payment failed | "
        f"Booking: {booking_id} | "
        f"Email: {email}"
    )


def booking_confirmation_task(
    email: str,
    booking_id: int,
):
    print(
        f"Booking confirmed | "
        f"Booking: {booking_id} | "
        f"Email: {email}"
    )