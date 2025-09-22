"""FastAPI application factory."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title="MCP Server",
        description="Model Context Protocol Server for secure directory browsing",
        version="0.1.0",
    )

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # TODO: Configure based on settings
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # TODO: Add routes and middleware
    return app