"""Workspace model for MCP Server."""
from pathlib import Path
from typing import NewType

from pydantic import BaseModel

# Type for workspace IDs
WorkspaceId = NewType("WorkspaceId", str)


class Workspace(BaseModel):
    """Model representing a workspace configuration."""

    id: WorkspaceId
    root_path: Path
    active: bool = True
    access_rules: list[str] = []

    @staticmethod
    def create(path: Path) -> WorkspaceId:
        """Create a new workspace ID from a path."""
        return WorkspaceId(str(path.resolve()))