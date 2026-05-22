import allure
from http import HTTPStatus
from clients.payment_client import PaymentClient
from clients.user_balance_client import UserBalanceClient
from schema.auth import UserLoginModel
from schema.payment import PaymentBaseModel, PaymentMessageModel
from schema.store_item import StoreItemModel
from schema.user_balance import UserBalanceModel, LowBalancePayloads
from tools.assertions.base import assert_status_code
from tools.assertions.payment import assert_pay_for_item, assert_payment_with_insufficient_balance
from tools.assertions.schema import validate_json_schema


@allure.epic('Payment')
class TestPayment:
    @allure.title('Can pay for the item')
    def test_pay_for_item(
            self,
            payment_client: PaymentClient,
            function_login: UserLoginModel,
            function_add_store_item: StoreItemModel,
            function_add_balance: UserBalanceModel
    ):
        response = payment_client.pay_for_item_api(
            function_login.user_id,
            function_add_store_item.item_id,
            function_login.token
        )
        model = PaymentBaseModel.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_pay_for_item(model, function_add_store_item, function_add_balance)

        validate_json_schema(response.json(), model.model_json_schema())

    @allure.title('Can not pay for the item if the balance is insufficient')
    def test_payment_with_insufficient_balance(
            self,
            payment_client: PaymentClient,
            user_balance_client: UserBalanceClient,
            function_login: UserLoginModel,
            function_add_store_item: StoreItemModel
    ):
        # ADD LOW BALANCE
        balance = LowBalancePayloads()
        user_balance_client.add_low_balance_api(function_login.user_id, balance, function_login.token)

        # BUY ITEM
        response = payment_client.pay_for_item_api(
            function_login.user_id,
            function_add_store_item.item_id,
            function_login.token
        )
        model = PaymentMessageModel.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.BAD_REQUEST)
        assert_payment_with_insufficient_balance(model, balance.balance, function_add_store_item)

        validate_json_schema(response.json(), model.model_json_schema())
