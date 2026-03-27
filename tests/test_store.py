from http import HTTPStatus
import allure
from clients.store_client import StoreClient
from schema.auth import UserLoginModel
from schema.store import StoreModel, StoreMessageModel, StoreErrorModel
from tools.assertions.base import assert_status_code
from tools.assertions.schema import validate_json_schema
from tools.assertions.store import assert_add_store, assert_add_store_twice, assert_unauthorized_error, \
    assert_get_store, get_not_found_store
from tools.fakers import fake


@allure.epic('Store')
class TestStore:
    @allure.title('Can add a new store')
    def test_add_store(self, store_client: StoreClient, function_login: UserLoginModel):
        store_name = fake.username()
        response = store_client.add_store_api(store_name, function_login.token)
        model = StoreModel.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.CREATED)
        assert_add_store(model, store_name)

        validate_json_schema(response.json(), model.model_json_schema())

    @allure.title('Can not add a store with existing store name')
    def test_add_store_twice(self, store_client: StoreClient, function_login: UserLoginModel):
        store_name = fake.username()
        response = store_client.add_store_twice_api(store_name, function_login.token)
        model = StoreMessageModel.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.BAD_REQUEST)
        assert_add_store_twice(model, store_name)

        validate_json_schema(response.json(), model.model_json_schema())

    @allure.title('Unauthorized user can not add a store')
    def test_add_store_without_auth_header(self, store_client: StoreClient):
        store_name = fake.username()
        response = store_client.add_store_without_aut_header_api(store_name)
        model = StoreErrorModel.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.UNAUTHORIZED)
        assert_unauthorized_error(model)

        validate_json_schema(response.json(), model.model_json_schema())

    @allure.title('Can get store info')
    def test_get_store(
            self,
            store_client: StoreClient,
            function_login: UserLoginModel,
            function_add_store: StoreModel
    ):
        response = store_client.get_store_api(function_add_store.name, function_login.token)
        model = StoreModel.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_get_store(model, function_add_store)

        validate_json_schema(response.json(), model.model_json_schema())

    @allure.title('Unauthorized user can not get the store info')
    def test_get_store_without_auth_header(self, store_client: StoreClient, function_add_store: StoreModel):
        response = store_client.get_store_without_aut_header_api(function_add_store.name)
        model = StoreErrorModel.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.UNAUTHORIZED)
        assert_unauthorized_error(model)

        validate_json_schema(response.json(), model.model_json_schema())

    @allure.title('Can not get the store with non-existent store name')
    def test_get_non_existent_store(self, store_client: StoreClient, function_login: UserLoginModel):
        response = store_client.get_not_existed_store_api(function_login.token)
        model = StoreMessageModel.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.NOT_FOUND)
        get_not_found_store(model)

        validate_json_schema(response.json(), model.model_json_schema())
