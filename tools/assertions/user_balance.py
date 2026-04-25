import allure
from schema.user_balance import UserBalanceModel, BalancePayloads, BalanceMessageModel
from tools.assertions.base import assert_equal
from tools.logger import get_logger

logger = get_logger("USER_BALANCE_ASSERTIONS")


@allure.step('Check add user balance')
def assert_add_user_balance(actual: UserBalanceModel, expected: BalancePayloads):
    logger.info('Check add user balance')

    assert_equal(
        actual.message,
        f'User balance has been updated. New balance is {float(expected.balance)}',
        'message'
    )
    assert_equal(actual.balance, expected.balance, 'balance')


@allure.step('Check get user balance')
def assert_get_user_balance(actual: UserBalanceModel, expected: UserBalanceModel):
    logger.info('Check get user balance')

    assert_equal(actual.message, f'User balance is {float(expected.balance)}', 'message')
    assert_equal(actual.balance, expected.balance, 'balance')


@allure.step('Check get empty user balance')
def assert_get_empty_user_balance(
        actual: BalanceMessageModel,
        expected: str = 'Balance not found. Add money for user.'
):
    logger.info('Check get empty user balance')

    assert_equal(actual.message, expected, 'message')
