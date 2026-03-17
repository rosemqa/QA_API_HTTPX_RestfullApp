import allure
from httpx import Response
from clients.base_client import BaseClient, get_http_client
from config import Settings
from schema.user_info import AddUserInfoPayloads, UpdateUserInfoPayloads
from tools.headers import Headers
from tools.routes import APIRoutes


class UserInfoClient(BaseClient):
    @allure.step('Add user info')
    def add_user_info_api(self, user_id: int, token: str, info: AddUserInfoPayloads) -> Response:
        return self.post(
            f'{APIRoutes.USER_INFO}/{user_id}',
            json=info.model_dump(mode='json'),
            headers=Headers.auth_header(token)
        )

    @allure.step('Edit user info by ID as authorized user')
    def update_user_info_api(self, user_id: int, token: str, info: UpdateUserInfoPayloads) -> Response:
        return self.put(
            f'{APIRoutes.USER_INFO}/{user_id}',
            json=info.model_dump(mode='json'),
            headers=Headers.auth_header(token)
        )

    @allure.step('Get the user info')
    def get_user_info_api(self, user_id: int, token: str) -> Response:
        return self.get(
            f'{APIRoutes.USER_INFO}/{user_id}',
            headers=Headers.auth_header(token)
        )

    @allure.step('Delete user info')
    def delete_user_info_api(self, user_id: int, token: str) -> Response:
        return self.delete(
            f'{APIRoutes.USER_INFO}/{user_id}',
            headers=Headers.auth_header(token)
        )

    def add_user_info(self, user_id: int, token: str):
        self.add_user_info_api(user_id, token, info=AddUserInfoPayloads())


def get_user_info_client(settings: Settings) -> UserInfoClient:
    return UserInfoClient(client=get_http_client(settings.http_client))
