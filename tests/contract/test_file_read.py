"""Test the file reading endpoint."""
import pytest
from fastapi import status

from src.models.workspace import WorkspaceId


@pytest.mark.asyncio
async def test_read_file_unauthorized(client):
    """Test that unauthorized requests are rejected."""
    response = await client.get("/api/v1/workspace/test/read")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_read_file_forbidden_path(client, valid_auth_token):
    """Test that attempts to access forbidden paths are rejected."""
    response = await client.get(
        "/api/v1/workspace/test/read",
        params={"path": "../forbidden.txt"},
        headers={"Authorization": f"Bearer {valid_auth_token}"},
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_read_file_success(client, valid_auth_token, test_workspace):
    """Test successful file reading."""
    # Create a test file
    test_file = test_workspace / "test.txt"
    content = "test content"
    test_file.write_text(content)

    response = await client.get(
        f"/api/v1/workspace/{WorkspaceId.create(test_workspace)}/read",
        params={"path": "test.txt"},
        headers={"Authorization": f"Bearer {valid_auth_token}"},
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["content"] == content
    assert "metadata" in data
    assert data["metadata"]["size"] == len(content)
    assert data["metadata"]["encoding"] == "utf-8"


@pytest.mark.asyncio
async def test_read_file_not_found(client, valid_auth_token, test_workspace):
    """Test reading a non-existent file."""
    response = await client.get(
        f"/api/v1/workspace/{WorkspaceId.create(test_workspace)}/read",
        params={"path": "nonexistent.txt"},
        headers={"Authorization": f"Bearer {valid_auth_token}"},
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_read_file_too_large(client, valid_auth_token, test_workspace):
    """Test reading a file that exceeds size limits."""
    # Create a large test file
    test_file = test_workspace / "large.txt"
    test_file.write_bytes(b"x" * (10 * 1024 * 1024 + 1))  # 10MB + 1 byte

    response = await client.get(
        f"/api/v1/workspace/{WorkspaceId.create(test_workspace)}/read",
        params={"path": "large.txt"},
        headers={"Authorization": f"Bearer {valid_auth_token}"},
    )
    assert response.status_code == status.HTTP_413_REQUEST_ENTITY_TOO_LARGE