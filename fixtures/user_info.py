import pytest

from clients.user_info_client import get_user_info_client, UserInfoClient
from config import Settings
from schema.auth import UserLoginModel


@pytest.fixture
def user_info_client(settings: Settings) -> UserInfoClient:
    return get_user_info_client(settings)


@pytest.fixture
def function_add_user_info(user_info_client: UserInfoClient, function_login: UserLoginModel):
    user_info_client.add_user_info(function_login.user_id, function_login.token)
