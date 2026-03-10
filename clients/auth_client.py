import allure
from httpx import Response
from clients.base_client import BaseClient, get_http_client
from config import Settings
from schema.auth import AuthModel
from tools.routes import APIRoutes


class AuthClient(BaseClient):
    @allure.step('Login with username and password')
    def auth_user_api(self, user_name: str = None, password: str = None) -> Response:
        return self.post(
            APIRoutes.AUTH,
            json={"username": user_name, "password": password}
        )


def get_auth_client(settings: Settings) -> AuthClient:
    return AuthClient(client=get_http_client(settings.http_client))
