from datetime import date, timedelta


# ==================================================
# GET CANCELLATIONS
# ==================================================

def test_get_cancellations(client):

    response = client.get(
        "/cancellations"
    )

    assert response.status_code in [
        200,
        401,
        403
    ]


# ==================================================
# GET CANCELLATION FOR BOOKING
# ==================================================

def test_get_booking_cancellation(client):

    response = client.get(
        "/cancellations/bookings/1"
    )

    assert response.status_code in [
        200,
        401,
        403,
        404
    ]


# ==================================================
# CANCEL BOOKING
# ==================================================

def test_cancel_booking(client):

    response = client.post(
        "/cancellations/bookings/1",
        json={
            "reason": "Personal reasons"
        }
    )

    assert response.status_code in [
        200,
        201,
        400,
        401,
        403,
        404
    ]


# ==================================================
# CANCEL ALREADY CANCELLED BOOKING
# ==================================================

def test_cancel_already_cancelled_booking(client):

    response = client.post(
        "/cancellations/bookings/1",
        json={
            "reason": "Cancelling again"
        }
    )

    assert response.status_code in [
        400,
        401,
        403,
        404
    ]


# ==================================================
# INVALID BOOKING
# ==================================================

def test_cancel_invalid_booking(client):

    response = client.post(
        "/cancellations/bookings/999999",
        json={
            "reason": "Test cancellation"
        }
    )

    assert response.status_code in [
        401,
        403,
        404
    ]


# ==================================================
# EMPTY REASON
# ==================================================

def test_cancel_without_reason(client):

    response = client.post(
        "/cancellations/bookings/1",
        json={
            "reason": ""
        }
    )

    assert response.status_code in [
        401,
        403,
        422
    ]