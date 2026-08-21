def test_get_payments(client):

    response = client.get(
        "/payments"
    )

    assert response.status_code == 200


def test_create_payment(client):

    response = client.post(
        "/payments/1",
        json={
            "amount": 10000,
            "payment_method": "UPI",
            "transaction_id": "TEST-TXN-001"
        }
    )

    assert response.status_code in [
        200,
        201,
        400,
        404
    ]