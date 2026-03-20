from http import HTTPStatus
import allure
from clients.user_info_client import UserInfoClient
from schema.auth import UserLoginModel
from schema.user_info import AddUserInfoPayloads, UserInfoBaseModel, GetUserInfoModel, UpdateUserInfoPayloads, \
    ErrorUserInfoModel
from tools.assertions.base import assert_status_code
from tools.assertions.schema import validate_json_schema
from tools.assertions.user_info import assert_add_user_info, assert_update_user_info, assert_get_user_info, \
    assert_delete_user_info, assert_get_non_existent_user_info, assert_unauthorized_error, assert_user_not_found, \
    assert_non_existent_user_info, assert_internal_server_error


class TestUserInfo:
    @allure.title('Can add the user info by user id')
    def test_add_user_info(self, check, user_info_client: UserInfoClient, function_login: UserLoginModel):
        # ADD USER INFO
        info = AddUserInfoPayloads()
        post_response = user_info_client.add_user_info_api(function_login.user_id, function_login.token, info)
        model = UserInfoBaseModel.model_validate_json(post_response.text)

        assert_status_code(post_response.status_code, HTTPStatus.OK)
        assert_add_user_info(model)

        validate_json_schema(post_response.json(), model.model_json_schema())

        # GET USER INFO
        get_response = user_info_client.get_user_info_api(function_login.user_id, function_login.token)
        get_model = GetUserInfoModel.model_validate_json(get_response.text)

        assert_status_code(get_response.status_code, HTTPStatus.OK)
        assert_get_user_info(check, get_model, info)

        validate_json_schema(get_response.json(), get_model.model_json_schema())

    @allure.title('Unable to add the user info as unauthorized user')
    def test_add_user_info_without_auth_token(self, user_info_client: UserInfoClient, function_login: UserLoginModel):
        response = user_info_client.add_user_info_without_auth_token_api(function_login.user_id)
        model = ErrorUserInfoModel.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.UNAUTHORIZED)
        assert_unauthorized_error(model)

        validate_json_schema(response.json(), model.model_json_schema())

    @allure.title('Unable to add the user info by non-existent user id')
    def test_add_user_info_by_non_existent_user_id(
            self,
            user_info_client: UserInfoClient,
            function_login: UserLoginModel
    ):
        user_id = 15000
        info = AddUserInfoPayloads()
        response = user_info_client.add_user_info_api(user_id, function_login.token, info)
        model = UserInfoBaseModel.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.NOT_FOUND)
        assert_user_not_found(model)

        validate_json_schema(response.json(), model.model_json_schema())

    @allure.title('Can update user info for authed user')
    def test_update_user_info(
            self,
            check,
            user_info_client: UserInfoClient,
            function_login: UserLoginModel,
            function_add_user_info
    ):
        # UPDATE USER INFO
        updated_info = UpdateUserInfoPayloads()
        response = user_info_client.update_user_info_api(function_login.user_id, function_login.token, updated_info)
        update_model = UserInfoBaseModel.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_update_user_info(update_model)

        validate_json_schema(response.json(), update_model.model_json_schema())

        # GET USER INFO
        get_response = user_info_client.get_user_info_api(function_login.user_id, function_login.token)
        get_model = GetUserInfoModel.model_validate_json(get_response.text)

        assert_status_code(get_response.status_code, HTTPStatus.OK)
        assert_get_user_info(check, get_model, updated_info)

    @allure.title('Unable to update the user info as unauthorized user')
    def test_update_user_info_without_auth_token(
            self,
            user_info_client: UserInfoClient,
            function_login: UserLoginModel
    ):
        response = user_info_client.update_user_info_without_auth_token_api(function_login.user_id)
        model = ErrorUserInfoModel.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.UNAUTHORIZED)
        assert_unauthorized_error(model)

        validate_json_schema(response.json(), model.model_json_schema())

    @allure.title('Unable to update the user info by non-existent user id')
    def test_update_user_info_by_non_existent_user_id(
            self,
            user_info_client: UserInfoClient,
            function_login: UserLoginModel
    ):
        user_id = 15000
        info = UpdateUserInfoPayloads()
        response = user_info_client.update_user_info_api(user_id, function_login.token, info)
        model = UserInfoBaseModel.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.NOT_FOUND)
        assert_non_existent_user_info(model)

        validate_json_schema(response.json(), model.model_json_schema())

    @allure.title('Can delete the user info')
    def test_delete_user_info(
            self,
            user_info_client: UserInfoClient,
            function_login: UserLoginModel,
            function_add_user_info
    ):
        # DELETE USER INFO
        del_response = user_info_client.delete_user_info_api(function_login.user_id, function_login.token)
        model = UserInfoBaseModel.model_validate_json(del_response.text)

        assert_status_code(del_response.status_code, HTTPStatus.OK)
        assert_delete_user_info(model)

        validate_json_schema(del_response.json(), model.model_json_schema())

        # GET USER  INFO
        get_response = user_info_client.get_user_info_api(function_login.user_id, function_login.token)
        get_model = UserInfoBaseModel.model_validate_json(get_response.text)

        assert_status_code(get_response.status_code, HTTPStatus.NOT_FOUND)
        assert_get_non_existent_user_info(get_model)

    @allure.title('Unable to delete the user info as unauthorized user')
    def test_delete_user_info_without_auth_token(
            self,
            user_info_client: UserInfoClient,
            function_login: UserLoginModel,
            function_add_user_info
    ):
        response = user_info_client.delete_user_info_without_auth_token_api(function_login.user_id)
        model = ErrorUserInfoModel.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.UNAUTHORIZED)
        assert_unauthorized_error(model)

        validate_json_schema(response.json(), model.model_json_schema())

    @allure.title('Check the error message when deleting the non_existent user info')
    def test_delete_non_existent_user_info(self, user_info_client: UserInfoClient, function_login: UserLoginModel):
        response = user_info_client.delete_user_info_api(function_login.user_id, function_login.token)
        model = UserInfoBaseModel.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.NOT_FOUND)
        assert_non_existent_user_info(model)

        validate_json_schema(response.json(), model.model_json_schema())

    @allure.title('Unable to get the user info as unauthorized user')
    def test_get_user_info_without_auth_token(
            self, user_info_client: UserInfoClient,
            function_login: UserLoginModel,
            function_add_user_info
    ):
        response = user_info_client.get_user_info_without_auth_token_api(function_login.user_id)
        model = ErrorUserInfoModel.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.UNAUTHORIZED)
        assert_unauthorized_error(model)

        validate_json_schema(response.json(), model.model_json_schema())

    @allure.title('Unable to get the user info by non-existent user id')
    def test_user_info_by_non_existent_user_id(
            self,
            user_info_client: UserInfoClient,
            function_login: UserLoginModel,
            function_add_user_info
    ):
        user_id = 1500
        response = user_info_client.get_user_info_api(user_id, function_login.token)
        model = UserInfoBaseModel.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.NOT_FOUND)
        assert_get_non_existent_user_info(model)

        validate_json_schema(response.json(), model.model_json_schema())

    @allure.title('Check for 500 internal server error for "get user info" request')
    def test_get_user_info_returns_500(
            self,
            user_info_client: UserInfoClient,
            function_login: UserLoginModel,
            function_add_user_info
    ):
        response = user_info_client.get_user_info_internal_server_error(function_login.user_id, function_login.token)
        model = ErrorUserInfoModel.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.INTERNAL_SERVER_ERROR)
        assert_internal_server_error(model)

        validate_json_schema(response.json(), model.model_json_schema())
