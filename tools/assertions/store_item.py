import allure
from schema.store_item import StoreItemModel, StoreItemPayloads, MessageModel, ItemErrorModel, AllItemsModel
from tools.assertions.base import assert_equal
from tools.logger import get_logger

logger = get_logger("STORE_ITEM_ASSERTIONS")


@allure.step('Check add/update store item')
def assert_add_store_item(check, actual: StoreItemModel, expected: StoreItemPayloads):
    logger.info("Check add/update store item")
    with check:
        assert_equal(str(actual.price), expected.price, 'price')
    with check:
        assert_equal(actual.description, expected.description, 'description')
    with check:
        assert_equal(actual.image, expected.image, 'image')


@allure.step('Check store item name for add store item')
def assert_store_item_name(actual: StoreItemModel, expected: str):
    logger.info("Check store item name for add store item")

    assert_equal(actual.name, expected, 'name')


@allure.step('Check add store item twice')
def asser_add_item_twice(actual: MessageModel, expected: str):
    logger.info("Check add store item twice")

    assert_equal(actual.message, f'An item with name {expected} already exists.', 'name')


@allure.step("Check unauthorized error")
def assert_unauthorized_error(actual: ItemErrorModel):
    logger.info("Check unauthorized error")

    assert_equal(actual.description, 'Request does not contain an access token', 'description')
    assert_equal(actual.error, 'Authorization Required', 'error')
    assert_equal(actual.status_code, 401, 'status_code')


@allure.step("Check add item with empty '{expected}' field")
def assert_add_item_with_empty_required_field(actual: MessageModel, expected: str):
    logger.info(f"Check add item with empty '{expected}' field")

    if expected == 'price':
        assert_equal(actual.message, {f"{expected}": "This field cannot be left blank!"}, 'message')
    else:
        assert_equal(actual.message, {f"{expected}": "Every item needs a store_id."}, 'message')


@allure.step('Check get store item')
def assert_get_store_item(actual: StoreItemModel, expected: StoreItemModel):
    logger.info("Check get store item")

    assert_equal(actual.name, expected.name, 'name')
    assert_equal(actual.price, expected.price, 'price')
    assert_equal(actual.description, expected.description, 'description')
    assert_equal(actual.image, expected.image, 'image')


@allure.step('Check get not found item')
def assert_get_not_found_item(actual: MessageModel, expected: str = 'Item not found'):
    logger.info("Check get not found item")

    assert_equal(actual.message, expected, 'message')


@allure.step('Check that item name "{item_name}" is in the item list')
def assert_item_name_in_item_list(item_name: str, item_list: AllItemsModel):
    logger.info(f"Check that item name '{item_name}' is in the item list")

    assert item_name in [i.name for i in item_list.items]
