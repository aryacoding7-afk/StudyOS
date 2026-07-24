API_PREFIX = "/api/v1"


def register_and_login(client):
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

    token = response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}",
    }


def test_create_note(client):
    headers = register_and_login(client)

    response = client.post(
        f"{API_PREFIX}/notes",
        json={
            "title": "My Note",
            "content": "Hello World",
        },
        headers=headers,
    )

    assert response.status_code == 201

    data = response.json()

    assert data["title"] == "My Note"
    assert data["content"] == "Hello World"
    assert "id" in data


def test_get_notes(client):
    headers = register_and_login(client)

    client.post(
        f"{API_PREFIX}/notes",
        json={
            "title": "Note 1",
            "content": "Content",
        },
        headers=headers,
    )

    response = client.get(
        f"{API_PREFIX}/notes",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) >= 1


def test_get_note_by_id(client):
    headers = register_and_login(client)

    create = client.post(
        f"{API_PREFIX}/notes",
        json={
            "title": "Test",
            "content": "Hello",
        },
        headers=headers,
    )

    note_id = create.json()["id"]

    response = client.get(
        f"{API_PREFIX}/notes/{note_id}",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == note_id
    assert data["title"] == "Test"


def test_update_note(client):
    headers = register_and_login(client)

    create = client.post(
        f"{API_PREFIX}/notes",
        json={
            "title": "Old",
            "content": "Old Content",
        },
        headers=headers,
    )

    note_id = create.json()["id"]

    response = client.put(
        f"{API_PREFIX}/notes/{note_id}",
        json={
            "title": "New",
            "content": "New Content",
        },
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == "New"
    assert data["content"] == "New Content"


def test_delete_note(client):
    headers = register_and_login(client)

    create = client.post(
        f"{API_PREFIX}/notes",
        json={
            "title": "Delete",
            "content": "Delete Me",
        },
        headers=headers,
    )

    note_id = create.json()["id"]

    response = client.delete(
        f"{API_PREFIX}/notes/{note_id}",
        headers=headers,
    )

    assert response.status_code == 204

    response = client.get(
        f"{API_PREFIX}/notes/{note_id}",
        headers=headers,
    )

    assert response.status_code == 404


def test_note_not_found(client):
    headers = register_and_login(client)

    response = client.get(
        f"{API_PREFIX}/notes/00000000-0000-0000-0000-000000000000",
        headers=headers,
    )

    assert response.status_code == 404


def test_notes_require_authentication(client):
    response = client.get(f"{API_PREFIX}/notes")

    assert response.status_code == 401