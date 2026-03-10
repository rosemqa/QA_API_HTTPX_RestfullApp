from http import HTTPStatus
import allure
import pytest
from clients.auth_client import AuthClient
from schema.auth import AuthModel, ErrorAuthModel
from schema.register import RegisterDataModel
from tools.assertions.auth import assert_login_with_empty_required_field
from tools.assertions.base import assert_status_code
from tools.assertions.schema import validate_json_schema
from tools.fakers import fake


@allure.epic('Auth')
class TestAuth:
    @allure.title('Can login with valid credentials')
    def test_auth_user(self, function_register: RegisterDataModel, auth_client: AuthClient):
        response = auth_client.auth_user_api(function_register.username, function_register.password)
        auth = AuthModel.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        validate_json_schema(response.json(), auth.model_json_schema())

    @allure.title('Cannot login with empty required fields')
    @pytest.mark.parametrize('empty_field', ['all', 'username', 'password'])
    def test_login_with_empty_required_field(
            self,
            function_register: RegisterDataModel,
            auth_client: AuthClient,
            empty_field
    ):
        if empty_field == 'all':
            response = auth_client.auth_user_api()
        elif empty_field == 'username':
            response = auth_client.auth_user_api(password=function_register.password)
        else:
            response = auth_client.auth_user_api(user_name=function_register.username)
        auth = ErrorAuthModel.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.UNAUTHORIZED)
        assert_login_with_empty_required_field(auth)
        validate_json_schema(response.json(), auth.model_json_schema())

    @allure.title('Cannot login with wrong email or password')
    @pytest.mark.parametrize('wrong_value', ['username', 'password'])
    def test_login_with_wrong_credentials(
            self,
            function_register: RegisterDataModel,
            auth_client: AuthClient,
            wrong_value
    ):
        if wrong_value == 'username':
            response = auth_client.auth_user_api(user_name=fake.username(), password=function_register.password)
        else:
            response = auth_client.auth_user_api(user_name=function_register.username, password=fake.password())
        auth = ErrorAuthModel.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.UNAUTHORIZED)
        assert_login_with_empty_required_field(auth)
        validate_json_schema(response.json(), auth.model_json_schema())
