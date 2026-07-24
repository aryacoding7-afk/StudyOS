from io import BytesIO
from pathlib import Path

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

    login = client.post(
        f"{API_PREFIX}/auth/login",
        json={
            "email": "arya@example.com",
            "password": "password123",
        },
    )

    token = login.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}",
    }


def test_upload_file(client):
    headers = register_and_login(client)

    pdf_path = Path("tests/sample.pdf")

    with pdf_path.open("rb") as f:
        response = client.post(
            f"{API_PREFIX}/files",
            files={
                "file": (
                    "sample.pdf",
                    f,
                    "application/pdf",
                )
            },
            headers=headers,
        )

    assert response.status_code == 201

    data = response.json()

    assert "file_id" in data
    assert "document_id" in data
    assert data["filename"] == "sample.pdf"

def test_upload_requires_auth(client):
    file_data = BytesIO(b"Hello")

    response = client.post(
        f"{API_PREFIX}/files",
        files={
            "file": (
                "test.txt",
                file_data,
                "text/plain",
            )
        },
    )

    assert response.status_code == 401


def test_upload_without_file(client):
    headers = register_and_login(client)

    response = client.post(
        f"{API_PREFIX}/files",
        headers=headers,
    )

    assert response.status_code == 422