def test_create_booking(client):

    response = client.post(
        "/bookings",
        json={
            "customer_id": 1,
            "package_id": 1,
            "booking_date": "2026-08-18",
            "number_of_travelers": 2,
            "discount": 1000,
            "tax": 500
        }
    )

    assert response.status_code in [200, 201]


def test_get_bookings(client):

    response = client.get(
        "/bookings"
    )

    assert response.status_code == 200


def test_booking_status_filter(client):

    response = client.get(
        "/bookings",
        params={
            "booking_status": "Pending"
        }
    )

    assert response.status_code == 200


def test_booking_pagination(client):

    response = client.get(
        "/bookings",
        params={
            "page": 1,
            "limit": 10
        }
    )

    assert response.status_code == 200