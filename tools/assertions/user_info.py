import allure
from schema.user_info import UserInfoBaseModel, AddUserInfoPayloads, GetUserInfoModel, UpdateUserInfoPayloads
from tools.assertions.base import assert_equal
from tools.logger import get_logger

logger = get_logger("USER_INFO_ASSERTIONS")


@allure.step("Check add user info")
def assert_add_user_info(actual: UserInfoBaseModel, expected: str = 'User info created successfully.'):
    logger.info("Check add user info")

    assert_equal(actual.message, expected, 'message')


@allure.step("Check update user info")
def assert_update_user_info(actual: UserInfoBaseModel, expected: str = 'User info updated successfully.'):
    logger.info("Check update user info")

    assert_equal(actual.message, expected, 'message')


@allure.step("Check get user info")
def assert_get_user_info(check, actual: GetUserInfoModel, expected: AddUserInfoPayloads | UpdateUserInfoPayloads):
    logger.info("Check get user info")
    with check:
        assert_equal(actual.city, expected.address.city, 'city')
    with check:
        assert_equal(actual.street, expected.address.street, 'street')
    with check:
        assert_equal(actual.phone, expected.phone, 'phone')
    with check:
        assert_equal(actual.email, expected.email, 'email')


@allure.step("Check delete user info")
def assert_delete_user_info(actual: UserInfoBaseModel, expected: str = 'User info deleted.'):
    logger.info("Check delete user info")

    assert_equal(actual.message, expected, 'message')


@allure.step("Check get non_existent/deleted user info")
def assert_get_non_existent_user_info(actual: UserInfoBaseModel, expected: str = 'User info not found'):
    logger.info("Check get non_existent/deleted user info")

    assert_equal(actual.message, expected, 'message')
