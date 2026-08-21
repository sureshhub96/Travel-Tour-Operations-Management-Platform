def test_create_guide(client):

    response = client.post(
        "/guides",
        json={
            "name": "Rahul Kumar",
            "email": "rahul.guide@example.com",
            "phone": "9876543210",
            "specialization": "Beach Tours",
            "availability_status": "Available"
        }
    )

    assert response.status_code in [200, 201]


def test_get_guides(client):

    response = client.get(
        "/guides"
    )

    assert response.status_code == 200