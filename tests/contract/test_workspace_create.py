"""Test the workspace management endpoints."""
import pytest
from fastapi import status


@pytest.mark.asyncio
async def test_create_workspace_unauthorized(client):
    """Test that unauthorized requests are rejected."""
    response = await client.post("/api/v1/workspace")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_create_workspace_success(client, valid_auth_token, test_workspace):
    """Test successful workspace creation."""
    response = await client.post(
        "/api/v1/workspace",
        json={
            "rootPath": str(test_workspace),
            "accessRules": ["**/*.py", "**/*.txt"],
        },
        headers={"Authorization": f"Bearer {valid_auth_token}"},
    )

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert "workspaceId" in data
    assert data["status"] == "active"
    assert "created" in data


@pytest.mark.asyncio
async def test_create_workspace_invalid_path(client, valid_auth_token):
    """Test workspace creation with invalid path."""
    response = await client.post(
        "/api/v1/workspace",
        json={
            "rootPath": "/nonexistent/path",
            "accessRules": ["**/*"],
        },
        headers={"Authorization": f"Bearer {valid_auth_token}"},
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.asyncio
async def test_create_workspace_invalid_rules(client, valid_auth_token, test_workspace):
    """Test workspace creation with invalid access rules."""
    response = await client.post(
        "/api/v1/workspace",
        json={
            "rootPath": str(test_workspace),
            "accessRules": ["../outside/*"],  # Path traversal attempt
        },
        headers={"Authorization": f"Bearer {valid_auth_token}"},
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST