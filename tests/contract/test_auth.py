"""Test the authentication endpoints."""
import pytest
from fastapi import status


@pytest.mark.asyncio
async def test_authenticate_success(client):
    """Test successful authentication."""
    response = await client.post(
        "/api/v1/auth",
        json={
            "provider": "github",
            "apiKey": "valid-key",
            "clientId": "test-client",
        },
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "token" in data
    assert "expires" in data
    assert "permissions" in data


@pytest.mark.asyncio
async def test_authenticate_invalid_credentials(client):
    """Test authentication with invalid credentials."""
    response = await client.post(
        "/api/v1/auth",
        json={
            "provider": "github",
            "apiKey": "invalid-key",
            "clientId": "test-client",
        },
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_authenticate_invalid_provider(client):
    """Test authentication with invalid provider."""
    response = await client.post(
        "/api/v1/auth",
        json={
            "provider": "invalid",
            "apiKey": "valid-key",
            "clientId": "test-client",
        },
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_authenticate_missing_fields(client):
    """Test authentication with missing required fields."""
    response = await client.post(
        "/api/v1/auth",
        json={
            "provider": "github",
        },
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY