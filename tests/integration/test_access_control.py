"""Test file access control functionality."""
import pytest
from fastapi import status

from src.models.workspace import WorkspaceId


@pytest.fixture
def access_control_workspace(tmp_path):
    """Create a workspace with various file types for access control testing."""
    workspace = tmp_path / "access_control"
    workspace.mkdir()
    # Create test directory structure
    (workspace / "public").mkdir()
    (workspace / "sensitive").mkdir()
    (workspace / "public/file.txt").write_text("public content")
    (workspace / "sensitive/secret.txt").write_text("sensitive content")
    (workspace / ".env").write_text("API_KEY=secret")
    return workspace


@pytest.mark.asyncio
async def test_file_access_control_rules(
    client, valid_auth_token, access_control_workspace
):
    """Test that file access control rules are properly enforced."""
    # Create workspace with access rules
    response = await client.post(
        "/api/v1/workspace",
        json={
            "rootPath": str(access_control_workspace),
            "accessRules": [
                "public/**/*",  # Allow public files
                "!sensitive/**/*",  # Deny sensitive files
                "!.env",  # Deny env file
            ],
        },
        headers={"Authorization": f"Bearer {valid_auth_token}"},
    )
    assert response.status_code == status.HTTP_201_CREATED
    workspace_id = response.json()["workspaceId"]

    # Test allowed public file
    response = await client.get(
        f"/api/v1/workspace/{workspace_id}/read",
        params={"path": "public/file.txt"},
        headers={"Authorization": f"Bearer {valid_auth_token}"},
    )
    assert response.status_code == status.HTTP_200_OK

    # Test denied sensitive file
    response = await client.get(
        f"/api/v1/workspace/{workspace_id}/read",
        params={"path": "sensitive/secret.txt"},
        headers={"Authorization": f"Bearer {valid_auth_token}"},
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN

    # Test denied env file
    response = await client.get(
        f"/api/v1/workspace/{workspace_id}/read",
        params={"path": ".env"},
        headers={"Authorization": f"Bearer {valid_auth_token}"},
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_file_type_restrictions(
    client, valid_auth_token, access_control_workspace
):
    """Test that file type restrictions are enforced."""
    # Create test files
    (access_control_workspace / "public/script.py").write_text("print('hello')")
    (access_control_workspace / "public/data.json").write_text('{"key": "value"}')
    (access_control_workspace / "public/binary.exe").write_bytes(b"\x00\x01")

    # Create workspace with file type restrictions
    response = await client.post(
        "/api/v1/workspace",
        json={
            "rootPath": str(access_control_workspace),
            "accessRules": [
                "public/*.{py,json}",  # Allow only Python and JSON files
            ],
        },
        headers={"Authorization": f"Bearer {valid_auth_token}"},
    )
    assert response.status_code == status.HTTP_201_CREATED
    workspace_id = response.json()["workspaceId"]

    # Test allowed Python file
    response = await client.get(
        f"/api/v1/workspace/{workspace_id}/read",
        params={"path": "public/script.py"},
        headers={"Authorization": f"Bearer {valid_auth_token}"},
    )
    assert response.status_code == status.HTTP_200_OK

    # Test allowed JSON file
    response = await client.get(
        f"/api/v1/workspace/{workspace_id}/read",
        params={"path": "public/data.json"},
        headers={"Authorization": f"Bearer {valid_auth_token}"},
    )
    assert response.status_code == status.HTTP_200_OK

    # Test denied binary file
    response = await client.get(
        f"/api/v1/workspace/{workspace_id}/read",
        params={"path": "public/binary.exe"},
        headers={"Authorization": f"Bearer {valid_auth_token}"},
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_file_size_restrictions(
    client, valid_auth_token, access_control_workspace
):
    """Test that file size restrictions are enforced."""
    large_file = access_control_workspace / "public/large.txt"
    large_file.write_bytes(b"x" * (10 * 1024 * 1024 + 1))  # 10MB + 1 byte

    # Create workspace
    response = await client.post(
        "/api/v1/workspace",
        json={
            "rootPath": str(access_control_workspace),
            "accessRules": ["public/**/*"],
        },
        headers={"Authorization": f"Bearer {valid_auth_token}"},
    )
    assert response.status_code == status.HTTP_201_CREATED
    workspace_id = response.json()["workspaceId"]

    # Test large file access
    response = await client.get(
        f"/api/v1/workspace/{workspace_id}/read",
        params={"path": "public/large.txt"},
        headers={"Authorization": f"Bearer {valid_auth_token}"},
    )
    assert response.status_code == status.HTTP_413_REQUEST_ENTITY_TOO_LARGE