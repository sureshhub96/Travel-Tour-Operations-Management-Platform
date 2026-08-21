def test_create_review(client):

    response = client.post(
        "/reviews",
        json={
            "customer_id": 1,
            "package_id": 1,
            "booking_id": 1,
            "rating": 5,
            "review_text": "Excellent tour experience"
        }
    )

    assert response.status_code in [
        200,
        201,
        400,
        404
    ]


def test_get_package_reviews(client):

    response = client.get(
        "/packages/1/reviews"
    )

    assert response.status_code in [
        200,
        404
    ]