import allure
from schema.register import CreateUserModel, MissingRequiredFieldModel
from tools.assertions.base import assert_equal
from tools.logger import get_logger

logger = get_logger("REGISTER_ASSERTIONS")


@allure.step("Check register user")
def assert_register_user(
        actual: CreateUserModel,
        expected: str = 'User created successfully.'
):
    logger.info("Check register user")
    assert_equal(actual.message,  expected, 'message')


@allure.step("Check create user with existing username")
def assert_register_user_twice(
        actual: CreateUserModel,
        expected: str = 'A user with that username already exists'
):
    logger.info("Check register user with existing username")
    assert_equal(actual.message,  expected, 'message')


@allure.step("Check create user without {expected} field")
def assert_create_user_without_required_field(
        actual: MissingRequiredFieldModel,
        expected: str
):
    logger.info(f"Check create user without '{expected}' field")
    if expected == 'username':
        assert_equal(actual.message, {"username": "This field cannot be blank."}, 'message')
    else:
        assert_equal(actual.message, {"password": "This field cannot be blank."}, 'message')
