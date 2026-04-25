import allure
from http import HTTPStatus
from clients.user_balance_client import UserBalanceClient
from schema.auth import UserLoginModel
from schema.user_balance import BalancePayloads, UserBalanceModel, BalanceMessageModel
from tools.assertions.base import assert_status_code
from tools.assertions.schema import validate_json_schema
from tools.assertions.user_balance import assert_add_user_balance, assert_get_user_balance, \
    assert_get_empty_user_balance


@allure.epic('User balance')
class TestUserBalance:
    @allure.title('Can add user balance')
    def test_add_user_balance(self, user_balance_client: UserBalanceClient, function_login: UserLoginModel):
        balance = BalancePayloads()
        response = user_balance_client.add_user_balance_api(function_login.user_id, balance, function_login.token)
        model = UserBalanceModel.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.CREATED)
        assert_add_user_balance(model, balance)

        validate_json_schema(response.json(), model.model_json_schema())

    @allure.title('Can get user balance')
    def test_get_user_balance(
            self,
            user_balance_client: UserBalanceClient,
            function_login: UserLoginModel,
            function_add_balance: UserBalanceModel
    ):
        response = user_balance_client.get_user_balance_api(function_login.user_id, function_login.token)
        model = UserBalanceModel.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_get_user_balance(model, function_add_balance)

        validate_json_schema(response.json(), model.model_json_schema())

    @allure.title('Can get an empty balance message')
    def test_get_empty_user_balance(self, user_balance_client: UserBalanceClient, function_login: UserLoginModel):
        response = user_balance_client.get_user_balance_api(function_login.user_id, function_login.token)
        model = BalanceMessageModel.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.NOT_FOUND)
        assert_get_empty_user_balance(model)

        validate_json_schema(response.json(), model.model_json_schema())
