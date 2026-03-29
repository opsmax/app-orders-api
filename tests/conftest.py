"""Shared test fixtures."""

import pytest
from httpx import ASGITransport, AsyncClient

from src.app.main import app


@pytest.fixture
def client():
    """Synchronous test client for the FastAPI app."""
    transport = ASGITransport(app=app)
    # httpx AsyncClient used synchronously via pytest-asyncio isn't needed;
    # use httpx in sync mode with the ASGI transport.
    from starlette.testclient import TestClient

    return TestClient(app)
