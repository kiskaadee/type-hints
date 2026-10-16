"""
Main FastAPI application factory.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from revex.server.routes import router


def create_app() -> FastAPI:
    """Factory creating and configuring the FastAPI app."""
    app = FastAPI(
        title="Revex Type Hints API",
        description="Stateless AST and Pyright validation server for modern Python type hints.",
        version="0.2.0",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configurable for web frontend
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(router)
    return app


app = create_app()
