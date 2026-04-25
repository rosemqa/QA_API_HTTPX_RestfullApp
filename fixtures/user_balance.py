import pytest
from clients.user_balance_client import UserBalanceClient, get_user_balance_client
from config import Settings
from schema.auth import UserLoginModel
from schema.user_balance import BalancePayloads, UserBalanceModel


@pytest.fixture
def user_balance_client(settings: Settings) -> UserBalanceClient:
    return get_user_balance_client(settings)


@pytest.fixture
def function_add_balance(user_balance_client: UserBalanceClient, function_login: UserLoginModel) -> UserBalanceModel:
    balance = BalancePayloads()
    response = user_balance_client.add_user_balance_api(function_login.user_id, balance, function_login.token)
    return UserBalanceModel.model_validate_json(response.text)
