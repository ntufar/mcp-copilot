"""Configuration management for MCP Server."""
from pydantic import BaseModel, Field


class SecurityConfig(BaseModel):
    """Security-related configuration."""

    max_file_size: int = Field(
        default=10 * 1024 * 1024,  # 10MB
        description="Maximum file size in bytes that can be read",
    )
    max_dir_entries: int = Field(
        default=1000,
        description="Maximum number of entries to return in directory listing",
    )
    allowed_mime_types: list[str] = Field(
        default=["text/*", "application/json"],
        description="List of allowed MIME type patterns",
    )


class RateLimitConfig(BaseModel):
    """Rate limiting configuration."""

    requests_per_minute: int = Field(
        default=100,
        description="Maximum number of requests per minute per client",
    )
    max_concurrent: int = Field(
        default=10,
        description="Maximum number of concurrent connections per client",
    )


class LogConfig(BaseModel):
    """Logging configuration."""

    level: str = Field(default="INFO", description="Logging level")
    format: str = Field(default="json", description="Log format (json or text)")
    audit_file: str = Field(
        default="audit.log",
        description="Path to the audit log file",
    )


class Config(BaseModel):
    """Main configuration."""

    security: SecurityConfig = Field(default_factory=SecurityConfig)
    rate_limit: RateLimitConfig = Field(default_factory=RateLimitConfig)
    log: LogConfig = Field(default_factory=LogConfig)
    debug: bool = Field(default=False, description="Enable debug mode")