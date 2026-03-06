from http import HTTPStatus
import allure
import pytest
from clients.register_client import RegisterClient
from schema.register import RegisterDataPayload, CreateUserModel, MissingRequiredFieldModel
from tools.assertions.base import assert_status_code
from tools.assertions.register import assert_register_user, assert_register_user_twice, \
    assert_create_user_without_required_field
from tools.assertions.schema import validate_json_schema


@allure.epic('Create user')
class TestRegister:
    @allure.title('Can create a new user')
    def test_create_user(self, register_client: RegisterClient):
        request = RegisterDataPayload()
        response = register_client.register_user_api(request)
        # register = CreateUserModel(**response.json()) # далает то же что и метод model_validate_json()
        # но ответ должен быть только в JSON формате
        register = CreateUserModel.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.CREATED)
        assert_register_user(register)

        validate_json_schema(
            response.json(), register.model_json_schema())  # по сути дублирует CreateUserModel.model_validate_json()

    @allure.title('Can not create user with existing username')
    def test_create_user_twice(self, register_client: RegisterClient):
        request = RegisterDataPayload()
        response = register_client.register_user_twice_api(request)
        register = CreateUserModel.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.BAD_REQUEST)
        assert_register_user_twice(register)

        validate_json_schema(response.json(), register.model_json_schema())

    @allure.title('Unable to create user if any of the required fields are missing')
    @pytest.mark.parametrize('missing_field', ['username', 'password'])
    def test_create_user_without_required_field(self, register_client, missing_field):
        request = RegisterDataPayload()
        response = register_client.register_user_without_required_field(request, missing_field)
        register = MissingRequiredFieldModel.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.BAD_REQUEST)
        assert_create_user_without_required_field(register, missing_field)

        validate_json_schema(response.json(), register.model_json_schema())
