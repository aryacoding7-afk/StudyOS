from pathlib import Path
from unittest.mock import patch

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


def upload_sample_pdf(client, headers):
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
    return response.json()["document_id"]


@patch("app.modules.search.service.generate_embedding")
def test_search_document(mock_embedding, client):
    mock_embedding.return_value = [0.1] * 384
    
    headers = register_and_login(client)
    document_id = upload_sample_pdf(client, headers)

    response = client.post(
        f"{API_PREFIX}/search",
        json={
            "document_id": document_id,
            "query": "hello",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "results" in data
    assert isinstance(data["results"], list)


def test_search_invalid_document(client):
    response = client.post(
        f"{API_PREFIX}/search",
        json={
            "document_id": "00000000-0000-0000-0000-000000000000",
            "query": "hello",
        },
    )

    # Adjust if your API returns a different code
    assert response.status_code in (200, 404)


def test_search_validation(client):
    response = client.post(
        f"{API_PREFIX}/search",
        json={
            "query": "hello",
        },
    )

    assert response.status_code == 422