def test_register_user(client):

    response = client.post(
        "/auth/register",
        json={
            "name": "Test User",
            "email": "testuser@example.com",
            "password": "Test@12345",
            "role": "Customer"
        }
    )

    assert response.status_code in [200, 201]


def test_register_duplicate_user(client):

    response = client.post(
        "/auth/register",
        json={
            "name": "Duplicate User",
            "email": "testuser@example.com",
            "password": "Test@12345",
            "role": "Customer"
        }
    )

    assert response.status_code in [400, 409]


def test_login_user(client):

    response = client.post(
        "/auth/login",
        json={
            "email": "testuser@example.com",
            "password": "Test@12345"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert "refresh_token" in data


def test_login_invalid_password(client):

    response = client.post(
        "/auth/login",
        json={
            "email": "testuser@example.com",
            "password": "WrongPassword123"
        }
    )

    assert response.status_code in [401, 400]