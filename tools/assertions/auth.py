import allure

from schema.auth import ErrorAuthModel
from tools.assertions.base import assert_equal
from tools.logger import get_logger

logger = get_logger("AUTH_ASSERTIONS")


@allure.step("Check login with empty/wrong required field")
def assert_login_with_empty_required_field(actual: ErrorAuthModel):
    logger.info("Check login with empty/wrong required field")

    assert_equal(actual.description, 'Invalid credentials', 'description')
    assert_equal(actual.error, 'Bad Request', 'error')
    assert_equal(actual.status_code, 401, 'status_code')
