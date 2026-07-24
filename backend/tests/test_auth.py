API_PREFIX = "/api/v1"


def test_register_user(client):
    response = client.post(
        f"{API_PREFIX}/auth/register",
        json={
            "username": "arya",
            "email": "arya@example.com",
            "password": "password123",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["username"] == "arya"
    assert data["email"] == "arya@example.com"
    assert "id" in data


def test_duplicate_email(client):
    client.post(
        f"{API_PREFIX}/auth/register",
        json={
            "username": "arya",
            "email": "arya@example.com",
            "password": "password123",
        },
    )

    response = client.post(
        f"{API_PREFIX}/auth/register",
        json={
            "username": "anotheruser",
            "email": "arya@example.com",
            "password": "password123",
        },
    )

    assert response.status_code == 409


def test_duplicate_username(client):
    client.post(
        f"{API_PREFIX}/auth/register",
        json={
            "username": "arya",
            "email": "arya@example.com",
            "password": "password123",
        },
    )

    response = client.post(
        f"{API_PREFIX}/auth/register",
        json={
            "username": "arya",
            "email": "different@example.com",
            "password": "password123",
        },
    )

    assert response.status_code == 409


def test_login_success(client):
    client.post(
        f"{API_PREFIX}/auth/register",
        json={
            "username": "arya",
            "email": "arya@example.com",
            "password": "password123",
        },
    )

    response = client.post(
        f"{API_PREFIX}/auth/login",
        json={
            "email": "arya@example.com",
            "password": "password123",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_password(client):
    client.post(
        f"{API_PREFIX}/auth/register",
        json={
            "username": "arya",
            "email": "arya@example.com",
            "password": "password123",
        },
    )

    response = client.post(
        f"{API_PREFIX}/auth/login",
        json={
            "email": "arya@example.com",
            "password": "wrongpassword",
        },
    )

    assert response.status_code == 401


def test_login_invalid_email(client):
    response = client.post(
        f"{API_PREFIX}/auth/login",
        json={
            "email": "doesnotexist@example.com",
            "password": "password123",
        },
    )

    assert response.status_code == 401


def test_get_current_user(client):
    client.post(
        f"{API_PREFIX}/auth/register",
        json={
            "username": "arya",
            "email": "arya@example.com",
            "password": "password123",
        },
    )

    login = client.post(
        f"{API_PREFIX}/auth/login",
        json={
            "email": "arya@example.com",
            "password": "password123",
        },
    )

    assert login.status_code == 200

    token = login.json()["access_token"]

    response = client.get(
        f"{API_PREFIX}/auth/me",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["username"] == "arya"
    assert data["email"] == "arya@example.com"