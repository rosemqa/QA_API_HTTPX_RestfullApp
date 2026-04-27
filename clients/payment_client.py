import allure
from clients.base_client import BaseClient, get_http_client
from config import Settings
from tools.headers import Headers
from tools.routes import APIRoutes


class PaymentClient(BaseClient):
    @allure.step('Pay for the item')
    def pay_for_item_api(self, user_id: int, item_id: int, token: str):
        response = self.post(
            f'{APIRoutes.PAYMENT}/{user_id}',
            json={"itemId": item_id},
            headers=Headers.auth_header(token)
        )
        return response


def get_payment_client(settings: Settings) -> PaymentClient:
    return PaymentClient(client=get_http_client(settings.http_client))
