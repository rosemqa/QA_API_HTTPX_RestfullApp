import pytest
from clients.store_client import StoreClient, get_store_client
from config import Settings
from schema.auth import UserLoginModel
from schema.store import StoreModel
from tools.fakers import fake


@pytest.fixture
def store_client(settings: Settings) -> StoreClient:
    return get_store_client(settings)


@pytest.fixture
def function_add_store(store_client: StoreClient, function_login: UserLoginModel) -> StoreModel:
    store_name = fake.username()
    response = store_client.add_store_api(store_name, function_login.token)
    return StoreModel.model_validate_json(response.text)
