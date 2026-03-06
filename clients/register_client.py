import allure
from httpx import Response
from clients.base_client import BaseClient, get_http_client
from config import Settings
from schema.register import RegisterDataPayload, CreateUserModel
from tools.routes import APIRoutes


class RegisterClient(BaseClient):
    @allure.step('Create a new user')
    def register_user_api(self, register: RegisterDataPayload) -> Response:
        return self.post(
            APIRoutes.REGISTER,
            json=register.model_dump(mode='json')
        )

    def register_user(self) -> CreateUserModel:
        """Упрощенный метод для создания нового пользователя"""
        # Создаем запрос с фейковыми данными (по умолчанию для теста)
        request = RegisterDataPayload()
        # Отправляем запрос на создание
        response = self.register_user_api(request)
        # Возвращаем созданного пользователя как объект схемы (модели)
        return CreateUserModel.model_validate_json(response.text)

    @allure.step('Create two users with the same username')
    def register_user_twice_api(self, register: RegisterDataPayload) -> Response:
        self.post(
            APIRoutes.REGISTER,
            json=register.model_dump(mode='json')
        )
        return self.post(
            APIRoutes.REGISTER,
            json=register.model_dump(mode='json')
        )

    def register_user_without_required_field(self, register: RegisterDataPayload, missing_field: str) -> Response:
        payloads = register.model_dump()
        del payloads[missing_field]
        return self.post(
            APIRoutes.REGISTER,
            json=payloads
        )


def get_register_client(settings: Settings) -> RegisterClient:
    """ Функция для создания экземпляра RegisterClient с нужными настройками."""
    return RegisterClient(client=get_http_client(settings.http_client))
