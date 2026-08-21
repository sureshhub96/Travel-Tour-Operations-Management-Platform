def test_create_activity(client):

    response = client.post(
        "/activities",
        json={
            "package_id": 1,
            "activity_name": "Scuba Diving",
            "location": "Baga Beach",
            "duration": 2,
            "price": 2500,
            "capacity": 10
        }
    )

    assert response.status_code in [200, 201]


def test_get_activities(client):

    response = client.get(
        "/activities"
    )

    assert response.status_code == 200