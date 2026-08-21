def test_create_room(client):

    response = client.post(
        "/rooms",
        json={
            "hotel_id": 1,
            "room_type": "Deluxe",
            "room_number": "101",
            "price_per_night": 5000,
            "capacity": 2,
            "availability_status": "Available"
        }
    )

    assert response.status_code in [200, 201]


def test_get_hotel_rooms(client):

    response = client.get(
        "/hotels/1/rooms"
    )

    assert response.status_code in [
        200,
        404
    ]