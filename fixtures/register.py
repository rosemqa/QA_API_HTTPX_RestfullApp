import pytest
from clients.register_client import get_register_client, RegisterClient
from config import Settings
from schema.register import RegisterDataModel


@pytest.fixture
def register_client(settings: Settings) -> RegisterClient:
    """Фикстура создаёт экземпляр API-клиента для работы с register"""
    return get_register_client(settings)


@pytest.fixture
def function_register(register_client: RegisterClient) -> RegisterDataModel:
    """Фикстура создает нового пользователя перед тестом и удаляет его после выполнения теста"""
    register = register_client.register_user()
    yield register
    # можно было бы дописать удаление пользователя "register_client.delete_user()" если бы был такой метод в API
