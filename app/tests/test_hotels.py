def test_create_hotel(client):

    response = client.post(
        "/hotels",
        json={
            "hotel_name": "Goa Beach Resort",
            "destination_id": 1,
            "address": "Calangute, Goa",
            "rating": 4.5,
            "contact_number": "9876543210"
        }
    )

    assert response.status_code in [200, 201]


def test_get_hotels(client):

    response = client.get(
        "/hotels"
    )

    assert response.status_code == 200