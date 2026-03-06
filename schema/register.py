from pydantic import BaseModel, Field
from tools.fakers import fake


class CreateUserModel(BaseModel):
    # model_config = ConfigDict(extra='forbid', strict=True)  # extra - валидирует на лишнии поля,
    # strict - не позволяет автоматически преобразовывать данные (строки в число)
    message: str
    uuid: int


class RegisterDataPayload(BaseModel):
    # model_config = ConfigDict(validate_default=True)  # validate_default можно указать и здесь

    username: str = Field(default_factory=fake.username, validate_default=True)
    # fake.username() писать без скобок - fake.username
    password: str = Field(default_factory=fake.password, validate_default=True)
    # без validate_default не будет проверять тип данных (str)


class RegisterDataModel(RegisterDataPayload):
    user_id: int


class MissingRequiredFieldModel(BaseModel):
    message: dict
