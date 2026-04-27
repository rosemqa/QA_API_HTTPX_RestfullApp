import pytest
from clients.payment_client import get_payment_client, PaymentClient
from config import Settings


@pytest.fixture
def payment_client(settings: Settings) -> PaymentClient:
    return get_payment_client(settings)
