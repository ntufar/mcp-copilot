"""Test fixtures for MCP Server tests."""
import pytest
from fastapi.testclient import TestClient

from src.api.app import create_app


@pytest.fixture
def app():
    """Create a test application instance."""
    return create_app()


@pytest.fixture
def client(app):
    """Create a test client."""
    return TestClient(app)


@pytest.fixture
def test_workspace(tmp_path):
    """Create a temporary workspace for testing."""
    workspace_dir = tmp_path / "test_workspace"
    workspace_dir.mkdir()
    return workspace_dir


@pytest.fixture
def valid_auth_token():
    """Create a valid authentication token for testing."""
    return "test-token"