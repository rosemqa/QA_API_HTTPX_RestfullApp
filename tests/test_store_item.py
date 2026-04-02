from http import HTTPStatus
import allure
import pytest
from clients.store_item_client import StoreItemClient
from schema.auth import UserLoginModel
from schema.store_item import StoreItemPayloads, StoreItemModel, MessageModel, ItemErrorModel, AllItemsModel
from tools.assertions.base import assert_status_code
from tools.assertions.schema import validate_json_schema
from tools.assertions.store_item import assert_add_store_item, assert_store_item_name, asser_add_item_twice, \
    assert_unauthorized_error, assert_add_item_with_empty_required_field, assert_get_store_item, \
    assert_get_not_found_item, assert_item_name_in_item_list
from tools.fakers import fake


@allure.epic('Store items')
class TestStoreItem:
    @allure.title('Can add a new item to the store')
    def test_add_new_item(self, check, store_item_client: StoreItemClient, function_login: UserLoginModel):
        item_name = fake.username()
        request = StoreItemPayloads()
        response = store_item_client.add_new_item_api(item_name, request, function_login.token)
        model = StoreItemModel.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.CREATED)
        assert_store_item_name(model, item_name)
        assert_add_store_item(check, model, request)

        validate_json_schema(response.json(), model.model_json_schema())

    @allure.title('Can not add a new item with existing name')
    def test_add_item_twice(self, store_item_client: StoreItemClient, function_login: UserLoginModel):
        item_name = fake.username()
        response = store_item_client.add_item_twice_api(item_name, function_login.token)
        model = MessageModel.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.BAD_REQUEST)
        asser_add_item_twice(model, item_name)

        validate_json_schema(response.json(), model.model_json_schema())

    @allure.title('Unauthorized user can not add the item')
    def test_item_without_auth_header(self, store_item_client: StoreItemClient):
        response = store_item_client.add_item_without_auth_header_api()
        model = ItemErrorModel.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.UNAUTHORIZED)
        assert_unauthorized_error(model)

        validate_json_schema(response.json(), model.model_json_schema())

    @allure.title('Unable to add an item if any of required fields are empty')
    @pytest.mark.parametrize('empty_field', ['price', 'store_id'])
    def test_add_item_with_empty_required_field(
            self,
            store_item_client: StoreItemClient,
            function_login: UserLoginModel,
            empty_field
    ):
        response = store_item_client.add_item_with_empty_required_field_api_api(empty_field, function_login.token)
        model = MessageModel.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.BAD_REQUEST)
        assert_add_item_with_empty_required_field(model, empty_field)

        validate_json_schema(response.json(), model.model_json_schema())

    @allure.title('Can get item info')
    def test_get_item(
            self,
            store_item_client: StoreItemClient,
            function_login: UserLoginModel,
            function_add_store_item: StoreItemModel
    ):
        response = store_item_client.get_store_item_api(function_add_store_item.name, function_login.token)
        model = StoreItemModel.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_get_store_item(model, function_add_store_item)

        validate_json_schema(response.json(), model.model_json_schema())

    @allure.title('Can not get item info by non-existent item name')
    def test_get_not_existed_item(self, store_item_client: StoreItemClient, function_login: UserLoginModel):
        response = store_item_client.get_not_existed_item_api(function_login.token)
        model = MessageModel.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.NOT_FOUND)
        assert_get_not_found_item(model)

        validate_json_schema(response.json(), model.model_json_schema())

    @allure.title('Unauthorized user can not get the item info')
    def test_get_item_without_auth_header(
            self,
            store_item_client: StoreItemClient,
            function_login: UserLoginModel,
            function_add_store_item: StoreItemModel
    ):
        response = store_item_client.get_item_without_auth_header_api(function_add_store_item.name)
        model = ItemErrorModel.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.UNAUTHORIZED)
        assert_unauthorized_error(model)

        validate_json_schema(response.json(), model.model_json_schema())

    @allure.description('Can edit item info')
    def test_update_item(
            self,
            check,
            store_item_client: StoreItemClient,
            function_login: UserLoginModel,
            function_add_store_item: StoreItemModel
    ):
        request = StoreItemPayloads()
        response = store_item_client.update_item_api(function_add_store_item.name, request, function_login.token)
        model = StoreItemModel.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_add_store_item(check, model, request)

        validate_json_schema(response.json(), model.model_json_schema())

    @allure.description('Can get the store item list, it contains the added item')
    def test_get_store_items(
            self,
            store_item_client: StoreItemClient,
            function_login: UserLoginModel,
            function_add_store_item: StoreItemModel
    ):
        item_name = function_add_store_item.name
        response = store_item_client.get_store_items_list_api(function_login.token)
        model = AllItemsModel.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_item_name_in_item_list(item_name, model)

        validate_json_schema(response.json(), model.model_json_schema())
