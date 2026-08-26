def test_signup(client):

    response = client.post(
        "/api/v1/auth/signup",
        json={
            "username": "customer@example.com",
            "firstname": "Test",
            "lastname": "Customer",
            "password": "Password123",
            "confirmpassword": "Password123",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["username"] == "customer@example.com"
    assert data["role"] == "customer"

    assert "password" not in data
    assert "password_hash" not in data

def test_password_mismatch(client):

    response = client.post(
        "/api/v1/auth/signup",
        json={
            "username": "test@example.com",
            "firstname": "Test",
            "lastname": "User",
            "password": "Password123",
            "confirmpassword": "Different123",
        },
    )

    assert response.status_code == 422

def test_duplicate_username(client):

    payload = {
        "username": "duplicate@example.com",
        "firstname": "Test",
        "lastname": "User",
        "password": "Password123",
        "confirmpassword": "Password123",
    }

    first = client.post(
        "/api/v1/auth/signup",
        json=payload,
    )

    assert first.status_code == 201

    second = client.post(
        "/api/v1/auth/signup",
        json=payload,
    )

    assert second.status_code == 409

def test_login(client):

    client.post(
        "/api/v1/auth/signup",
        json={
            "username": "login@example.com",
            "firstname": "Login",
            "lastname": "User",
            "password": "Password123",
            "confirmpassword": "Password123",
        },
    )

    response = client.post(
        "/api/v1/auth/login",
        json={
            "username": "login@example.com",
            "password": "Password123",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert "refresh_token" in data