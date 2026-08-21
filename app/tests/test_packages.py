def test_create_package(client):

    response = client.post(
        "/packages",
        json={
            "package_name": "Goa Holiday",
            "destination_id": 1,
            "description": "Five day Goa tour",
            "duration_days": 5,
            "base_price": 25000,
            "max_capacity": 20,
            "available_slots": 20,
            "start_date": "2026-09-01",
            "end_date": "2026-09-05",
            "status": "Published"
        }
    )

    assert response.status_code in [200, 201]


def test_get_packages(client):

    response = client.get(
        "/packages"
    )

    assert response.status_code == 200

    assert isinstance(
        response.json(),
        list
    )


def test_package_price_filter(client):

    response = client.get(
        "/packages",
        params={
            "min_price": 10000,
            "max_price": 50000
        }
    )

    assert response.status_code == 200