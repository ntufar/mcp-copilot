"""Test the directory listing endpoint."""
import pytest
from fastapi import status

from src.models.workspace import WorkspaceId


@pytest.mark.asyncio
async def test_list_directory_unauthorized(client):
    """Test that unauthorized requests are rejected."""
    response = await client.get("/api/v1/workspace/test/list")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_list_directory_forbidden_path(client, valid_auth_token):
    """Test that attempts to access forbidden paths are rejected."""
    response = await client.get(
        "/api/v1/workspace/test/list",
        params={"path": "../forbidden"},
        headers={"Authorization": f"Bearer {valid_auth_token}"},
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_list_directory_success(client, valid_auth_token, test_workspace):
    """Test successful directory listing."""
    # Create a test file in the workspace
    test_file = test_workspace / "test.txt"
    test_file.write_text("test content")

    response = await client.get(
        f"/api/v1/workspace/{WorkspaceId.create(test_workspace)}/list",
        headers={"Authorization": f"Bearer {valid_auth_token}"},
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "entries" in data
    assert len(data["entries"]) == 1
    assert data["entries"][0]["name"] == "test.txt"
    assert data["entries"][0]["type"] == "file"
    assert "metadata" in data
    assert data["metadata"]["totalEntries"] == 1


@pytest.mark.asyncio
async def test_list_directory_not_found(client, valid_auth_token):
    """Test listing a non-existent directory."""
    response = await client.get(
        "/api/v1/workspace/nonexistent/list",
        headers={"Authorization": f"Bearer {valid_auth_token}"},
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND