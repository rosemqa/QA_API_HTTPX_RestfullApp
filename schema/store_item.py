from pydantic import Field, BaseModel, HttpUrl
from tools.fakers import fake


class StoreItemPayloads(BaseModel):
    price: str = Field(default_factory=fake.price)
    store_id: int = 1
    description: str = Field(default_factory=fake.item_description)
    image: HttpUrl = Field(default_factory=fake.image_url)


class StoreItemModel(BaseModel):
    name: str
    price: int
    item_id: int = Field(alias='itemID')
    description: str
    image: str


class MessageModel(BaseModel):
    message: str | dict


class ItemErrorModel(BaseModel):
    description: str
    error: str
    status_code: int


class AllItemsModel(BaseModel):
    items: list[StoreItemModel]
