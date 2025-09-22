"""Test workspace isolation functionality."""
import asyncio

import pytest
from fastapi import status

from src.models.workspace import WorkspaceId


@pytest.fixture
def isolated_workspace(tmp_path):
    """Create an isolated workspace for testing."""
    workspace = tmp_path / "isolated"
    workspace.mkdir()
    # Create some test files and directories
    (workspace / "allowed").mkdir()
    (workspace / "allowed/file.txt").write_text("test content")
    return workspace


@pytest.mark.asyncio
async def test_workspace_isolation_boundaries(client, valid_auth_token, isolated_workspace):
    """Test that workspaces are properly isolated."""
    # Create workspace
    response = await client.post(
        "/api/v1/workspace",
        json={
            "rootPath": str(isolated_workspace),
            "accessRules": ["allowed/**/*"],
        },
        headers={"Authorization": f"Bearer {valid_auth_token}"},
    )
    assert response.status_code == status.HTTP_201_CREATED
    workspace_id = response.json()["workspaceId"]

    # Test allowed path
    response = await client.get(
        f"/api/v1/workspace/{workspace_id}/read",
        params={"path": "allowed/file.txt"},
        headers={"Authorization": f"Bearer {valid_auth_token}"},
    )
    assert response.status_code == status.HTTP_200_OK

    # Test path traversal
    response = await client.get(
        f"/api/v1/workspace/{workspace_id}/read",
        params={"path": "../outside.txt"},
        headers={"Authorization": f"Bearer {valid_auth_token}"},
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN

    # Test absolute path
    response = await client.get(
        f"/api/v1/workspace/{workspace_id}/read",
        params={"path": "/etc/passwd"},
        headers={"Authorization": f"Bearer {valid_auth_token}"},
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_workspace_access_rules(client, valid_auth_token, isolated_workspace):
    """Test that access rules are properly enforced."""
    # Create workspace with specific rules
    response = await client.post(
        "/api/v1/workspace",
        json={
            "rootPath": str(isolated_workspace),
            "accessRules": [
                "allowed/*.txt",  # Allow txt files in allowed directory
                "!allowed/*.log",  # Deny log files
            ],
        },
        headers={"Authorization": f"Bearer {valid_auth_token}"},
    )
    assert response.status_code == status.HTTP_201_CREATED
    workspace_id = response.json()["workspaceId"]

    # Create test files
    (isolated_workspace / "allowed/test.txt").write_text("allowed")
    (isolated_workspace / "allowed/test.log").write_text("denied")

    # Test allowed file
    response = await client.get(
        f"/api/v1/workspace/{workspace_id}/read",
        params={"path": "allowed/test.txt"},
        headers={"Authorization": f"Bearer {valid_auth_token}"},
    )
    assert response.status_code == status.HTTP_200_OK

    # Test denied file
    response = await client.get(
        f"/api/v1/workspace/{workspace_id}/read",
        params={"path": "allowed/test.log"},
        headers={"Authorization": f"Bearer {valid_auth_token}"},
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_workspace_concurrent_access(
    client, valid_auth_token, isolated_workspace
):
    """Test that concurrent access to workspace is handled properly."""
    # Create workspace
    response = await client.post(
        "/api/v1/workspace",
        json={
            "rootPath": str(isolated_workspace),
            "accessRules": ["allowed/**/*"],
        },
        headers={"Authorization": f"Bearer {valid_auth_token}"},
    )
    assert response.status_code == status.HTTP_201_CREATED
    workspace_id = response.json()["workspaceId"]

    # Create a test file
    test_file = isolated_workspace / "allowed/concurrent.txt"
    test_file.write_text("test content")

    # Simulate concurrent reads
    tasks = []
    for _ in range(10):
        tasks.append(
            client.get(
                f"/api/v1/workspace/{workspace_id}/read",
                params={"path": "allowed/concurrent.txt"},
                headers={"Authorization": f"Bearer {valid_auth_token}"},
            )
        )

    # All requests should succeed
    responses = await asyncio.gather(*tasks)
    for response in responses:
        assert response.status_code == status.HTTP_200_OK