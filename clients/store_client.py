import allure
from httpx import Response
from clients.base_client import BaseClient, get_http_client
from config import Settings
from tools.headers import Headers
from tools.routes import APIRoutes


class StoreClient(BaseClient):
    @allure.step('Add a new store')
    def add_store_api(self, store_name: str, token: str) -> Response:
        return self.post(
            f'{APIRoutes.STORE}/{store_name}',
            headers=Headers.auth_header(token)
        )

    @allure.step('Add two stores with the same name')
    def add_store_twice_api(self, store_name: str, token: str) -> Response:
        self.post(
            f'{APIRoutes.STORE}/{store_name}',
            headers=Headers.auth_header(token)
        )
        return self.post(
            f'{APIRoutes.STORE}/{store_name}',
            headers=Headers.auth_header(token)
        )

    @allure.step('Add store as unauthorized user')
    def add_store_without_aut_header_api(self, store_name: str) -> Response:
        return self.post(f'{APIRoutes.STORE}/{store_name}')

    @allure.step('Get store as authorized user')
    def get_store_api(self, store_name: str, token: str) -> Response:
        return self.get(
            f'{APIRoutes.STORE}/{store_name}',
            headers=Headers.auth_header(token)
        )

    @allure.step('Get store as unauthorized user')
    def get_store_without_aut_header_api(self, store_name: str) -> Response:
        return self.get(f'{APIRoutes.STORE}/{store_name}')

    @allure.step('Get store with not existed name')
    def get_not_existed_store_api(self, token: str) -> Response:
        store_name = 'fake_store'
        return self.get(
            f'{APIRoutes.STORE}/{store_name}',
            headers=Headers.auth_header(token)
        )


def get_store_client(settings: Settings) -> StoreClient:
    return StoreClient(client=get_http_client(settings.http_client))
