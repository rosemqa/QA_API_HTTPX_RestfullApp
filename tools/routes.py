from enum import Enum


class APIRoutes(str, Enum):
    REGISTER = '/register'
    # USER_INFO = lambda user_id: f'/user_info/{user_id}'
    USER_INFO = '/user_info/'
    AUTH = '/auth'

    def __str__(self):
        return self.value
