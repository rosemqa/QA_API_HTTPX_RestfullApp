import allure
from clients.base_client import BaseClient, get_http_client
from config import Settings
from schema.store_item import StoreItemPayloads
from tools.fakers import fake
from tools.headers import Headers
from tools.routes import APIRoutes


class StoreItemClient(BaseClient):
    @allure.step('Add a new item to the store')
    def add_new_item_api(self, item_name: str, item: StoreItemPayloads, token: str):
        return self.post(
            f'{APIRoutes.STORE_ITEM}/{item_name}',
            json=item.model_dump(),
            headers=Headers.auth_header(token)
        )

    @allure.step('Add two items with the same name')
    def add_item_twice_api(self, item_name: str, token: str):
        item = StoreItemPayloads()
        for i in range(2):
            response = self.post(
                f'{APIRoutes.STORE_ITEM}/{item_name}',
                json=item.model_dump(),
                headers=Headers.auth_header(token)
            )
            if i == 1:
                return response

    @allure.step('Add item as unauthorized user')
    def add_item_without_auth_header_api(self):
        item = StoreItemPayloads()
        item_name = fake.username()
        return self.post(
            f'{APIRoutes.STORE_ITEM}/{item_name}',
            json=item.model_dump()
        )

    @allure.step('Add item with empty required field')
    def add_item_with_empty_required_field_api(self, empty_field: str, token: str):
        item_name = fake.username()
        item = StoreItemPayloads().model_dump()
        item[empty_field] = ''
        return self.post(
            f'{APIRoutes.STORE_ITEM}/{item_name}',
            json=item,
            headers=Headers.auth_header(token)
        )

    @allure.step('Get item info by item_name as authorized user')
    def get_store_item_api(self, item_name: str, token: str):
        return self.get(
            f'{APIRoutes.STORE_ITEM}/{item_name}',
            headers=Headers.auth_header(token)
        )

    @allure.step('Get item info by not-existed item_name')
    def get_not_existed_item_api(self, token: str):
        fake_item_name = fake.username()
        return self.get(
            f'{APIRoutes.STORE_ITEM}/{fake_item_name}',
            headers=Headers.auth_header(token)
        )

    @allure.step('Get item info by not-existed item_name')
    def get_item_without_auth_header_api(self, item_name: str):
        return self.get(
            f'{APIRoutes.STORE_ITEM}/{item_name}'
        )

    @allure.step('Edit item info by item name as authorized user')
    def update_item_api(self, item_name: str, item: StoreItemPayloads, token: str):
        return self.put(
            f'{APIRoutes.STORE_ITEM}/{item_name}',
            json=item.model_dump(),
            headers=Headers.auth_header(token)
        )

    @allure.step('Get a list of store items')
    def get_store_items_list_api(self,  token: str):
        return self.get(
            APIRoutes.STORE_ITEMS,
            headers=Headers.auth_header(token)
        )


def get_store_item_client(settings: Settings) -> StoreItemClient:
    return StoreItemClient(client=get_http_client(settings.http_client))
