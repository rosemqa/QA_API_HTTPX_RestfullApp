import allure
from schema.store import StoreModel, StoreMessageModel, StoreErrorModel
from tools.assertions.base import assert_equal
from tools.logger import get_logger

logger = get_logger("STORE_ASSERTIONS")


@allure.step('Check add store')
def assert_add_store(actual: StoreModel, expected):
    logger.info('Check add store')

    assert_equal(actual.name, expected, 'name')


@allure.step('Check add store tice')
def assert_add_store_twice(actual: StoreMessageModel, expected):
    logger.info('Check add store twice')

    assert_equal(actual.message, f"A store with name '{expected}' already exists.", 'message')


@allure.step("Check unauthorized error")
def assert_unauthorized_error(actual: StoreErrorModel):
    logger.info("Check unauthorized error")

    assert_equal(actual.description, 'Request does not contain an access token', 'description')
    assert_equal(actual.error, 'Authorization Required', 'error')
    assert_equal(actual.status_code, 401, 'status_code')


@allure.step('Check get store')
def assert_get_store(actual: StoreModel, expected: StoreModel):
    logger.info('Check get store')

    assert_equal(actual.name, expected.name, 'name')


@allure.step('Check get store with not existed name')
def get_not_found_store(actual: StoreMessageModel, expected: str = 'Store not found'):
    logger.info('Check get store with not existed name')

    assert_equal(actual.message, expected, 'message')
