import pytest
from clients.store_item_client import StoreItemClient, get_store_item_client
from config import Settings
from schema.auth import UserLoginModel
from schema.store_item import StoreItemModel, StoreItemPayloads
from tools.fakers import fake


@pytest.fixture
def store_item_client(settings: Settings) -> StoreItemClient:
    return get_store_item_client(settings)


@pytest.fixture
def function_add_store_item(store_item_client: StoreItemClient, function_login: UserLoginModel) -> StoreItemModel:
    item_name = fake.username()
    request = StoreItemPayloads()
    response = store_item_client.add_new_item_api(item_name, request, function_login.token)
    return StoreItemModel.model_validate_json(response.text)
