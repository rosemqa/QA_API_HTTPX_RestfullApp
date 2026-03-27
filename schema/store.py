from pydantic import BaseModel


class StoreModel(BaseModel):
    name: str
    items: list[str]
    uuid: int


class StoreMessageModel(BaseModel):
    message: str


class StoreErrorModel(BaseModel):
    description: str
    error: str
    status_code: int
