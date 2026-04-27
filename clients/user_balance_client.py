import allure
from clients.base_client import BaseClient, get_http_client
from config import Settings
from schema.user_balance import BalancePayloads, LowBalancePayloads
from tools.headers import Headers
from tools.routes import APIRoutes


class UserBalanceClient(BaseClient):
    @allure.step('Add user balance')
    def add_user_balance_api(self, user_id: int, balance: BalancePayloads, token: str):
        response = self.post(
            f'{APIRoutes.USER_BALANCE}/{user_id}',
            json=balance.model_dump(),
            headers=Headers.auth_header(token)
        )
        return response

    @allure.step('Add low user balance (0-5)')
    def add_low_balance_api(self, user_id: int, balance: LowBalancePayloads, token: str):
        response = self.post(
            f'{APIRoutes.USER_BALANCE}/{user_id}',
            json=balance.model_dump(),
            headers=Headers.auth_header(token)
        )
        return response

    @allure.step('Get user balance')
    def get_user_balance_api(self, user_id: int, token: str):
        response = self.get(
            f'{APIRoutes.USER_BALANCE}/{user_id}',
            headers=Headers.auth_header(token)
        )
        return response


def get_user_balance_client(settings: Settings) -> UserBalanceClient:
    return UserBalanceClient(client=get_http_client(settings.http_client))
