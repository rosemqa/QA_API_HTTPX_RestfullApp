import pytest
from clients.auth_client import get_auth_client, AuthClient
from config import Settings


@pytest.fixture
def auth_client(settings: Settings) -> AuthClient:
    return get_auth_client(settings)
