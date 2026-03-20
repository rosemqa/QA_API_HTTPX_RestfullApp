import allure
from schema.user_info import UserInfoBaseModel, AddUserInfoPayloads, GetUserInfoModel, UpdateUserInfoPayloads, \
    ErrorUserInfoModel
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


@allure.step("Check update non_existent user info")
def assert_non_existent_user_info(actual: UserInfoBaseModel, expected: str = 'User info not found.'):
    logger.info("Check update non_existent user info")

    assert_equal(actual.message, expected, 'message')


@allure.step("Check unauthorized error")
def assert_unauthorized_error(actual: ErrorUserInfoModel):
    logger.info("Check unauthorized error")

    expected = {
        "description": "Request does not contain an access token",
        "error": "Authorization Required",
        "status_code": 401
    }

    assert_equal(actual.description, expected['description'], 'description')
    assert_equal(actual.error, expected['error'], 'error')
    assert_equal(actual.status_code, expected['status_code'], 'status_code')


@allure.step("Check user not found")
def assert_user_not_found(actual: UserInfoBaseModel, expected: str = 'User not found'):
    logger.info("Check user not found")

    assert_equal(actual.message, expected, 'message')


@allure.step("Check internal server error")
def assert_internal_server_error(actual: ErrorUserInfoModel):
    logger.info("Check internal server error")

    assert_equal(actual.description, 'Server Error', 'description')
    assert_equal(actual.error, 'Internal Error Server', 'error')
    assert_equal(actual.status_code, 500, 'status_code')
