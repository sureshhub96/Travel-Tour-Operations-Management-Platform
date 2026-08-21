import re
from datetime import date, time


# ==================================================
# EMAIL
# ==================================================

def validate_email(email: str) -> str:

    email = email.strip().lower()

    pattern = (
        r"^[A-Za-z0-9._%+-]+"
        r"@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    )

    if not re.match(pattern, email):
        raise ValueError(
            "Invalid email address"
        )

    return email


# ==================================================
# PHONE
# ==================================================

def validate_phone(phone: str) -> str:

    phone = phone.strip()

    pattern = r"^\+?[0-9][0-9\s-]{8,14}$"

    if not re.match(pattern, phone):
        raise ValueError(
            "Invalid phone number"
        )

    return phone


# ==================================================
# PASSWORD
# ==================================================

def validate_password(password: str) -> str:

    if not password:
        raise ValueError(
            "Password is required"
        )

    if len(password) < 8:
        raise ValueError(
            "Password must contain at least 8 characters"
        )

    if len(password.encode("utf-8")) > 72:
        raise ValueError(
            "Password cannot exceed 72 bytes"
        )

    return password


# ==================================================
# POSITIVE NUMBER
# ==================================================

def validate_positive_number(
    value: float,
    field_name: str = "Value"
) -> float:

    if value <= 0:
        raise ValueError(
            f"{field_name} must be greater than 0"
        )

    return value


# ==================================================
# NON-NEGATIVE NUMBER
# ==================================================

def validate_non_negative(
    value: float,
    field_name: str = "Value"
) -> float:

    if value < 0:
        raise ValueError(
            f"{field_name} cannot be negative"
        )

    return value


# ==================================================
# POSITIVE INTEGER
# ==================================================

def validate_positive_integer(
    value: int,
    field_name: str = "Value"
) -> int:

    if value <= 0:
        raise ValueError(
            f"{field_name} must be greater than 0"
        )

    return value


# ==================================================
# DATE RANGE
# ==================================================

def validate_date_range(
    start_date: date,
    end_date: date
) -> bool:

    if end_date <= start_date:
        raise ValueError(
            "End date must be after start date"
        )

    return True


# ==================================================
# TIME RANGE
# ==================================================

def validate_time_range(
    start_time: time,
    end_time: time
) -> bool:

    if end_time <= start_time:
        raise ValueError(
            "End time must be after start time"
        )

    return True


# ==================================================
# CAPACITY
# ==================================================

def validate_capacity(
    capacity: int,
    available_slots: int | None = None
) -> bool:

    if capacity <= 0:
        raise ValueError(
            "Capacity must be greater than 0"
        )

    if available_slots is not None:

        if available_slots < 0:
            raise ValueError(
                "Available slots cannot be negative"
            )

        if available_slots > capacity:
            raise ValueError(
                "Available slots cannot exceed capacity"
            )

    return True


# ==================================================
# RATING
# ==================================================

def validate_rating(
    rating: float
) -> float:

    if rating < 1 or rating > 5:
        raise ValueError(
            "Rating must be between 1 and 5"
        )

    return rating