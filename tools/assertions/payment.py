import allure
from schema.payment import PaymentBaseModel, PaymentMessageModel
from schema.store_item import StoreItemModel
from schema.user_balance import UserBalanceModel
from tools.assertions.base import assert_equal
from tools.logger import get_logger

logger = get_logger("PAYMENT_ASSERTIONS")


@allure.step('Check pay for item')
def assert_pay_for_item(actual: PaymentBaseModel, expected: StoreItemModel, initial_balance: UserBalanceModel):
    logger.info('Check pay for item')
    current_balance = initial_balance.balance - expected.price

    assert_equal(actual.message, "Payment was successful", 'message')
    assert_equal(actual.balance, current_balance, 'balance')
    assert_equal(actual.name, expected.name, 'name')
    assert_equal(actual.price, expected.price, 'price')


@allure.step('Check payment with insufficient balance')
def assert_payment_with_insufficient_balance(actual: PaymentMessageModel, balance: int, item: StoreItemModel):
    logger.info('Check payment with insufficient balance')

    assert_equal(
        actual.message,
        f'Not enough money. Your balance is {float(balance)}, item cost {float(item.price)}',
        'message'
    )
