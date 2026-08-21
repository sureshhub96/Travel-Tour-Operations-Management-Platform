def test_create_destination(client):

    response = client.post(
        "/destinations",
        json={
            "name": "Goa",
            "country": "India",
            "state": "Goa",
            "description": "Beautiful beach destination",
            "best_season": "Winter",
            "status": "Active"
        }
    )

    assert response.status_code in [200, 201]


def test_get_destinations(client):

    response = client.get(
        "/destinations"
    )

    assert response.status_code == 200

    assert isinstance(
        response.json(),
        list
    )