from enum import Enum


class APIRoutes(str, Enum):
    REGISTER = '/register'
    # USER_INFO = lambda user_id: f'/user_info/{user_id}'
    USER_INFO = '/user_info'
    AUTH = '/auth'
    STORE = '/store'
    STORE_ITEM = '/item'
    STORE_ITEMS = '/items'
    USER_BALANCE = '/balance'
    PAYMENT = '/pay'

    def __str__(self):
        return self.value
