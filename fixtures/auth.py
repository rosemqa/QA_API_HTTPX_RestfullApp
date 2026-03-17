import pytest
from clients.auth_client import get_auth_client, AuthClient
from config import Settings
from schema.auth import UserLoginModel
from schema.register import RegisterDataModel


@pytest.fixture
def auth_client(settings: Settings) -> AuthClient:
    return get_auth_client(settings)


@pytest.fixture
def function_login(auth_client: AuthClient, function_register: RegisterDataModel) -> UserLoginModel:
    token = auth_client.login_user(function_register.username, function_register.password)
    return UserLoginModel(user_id=function_register.user_id, token=token.access_token)
