from pydantic import BaseModel


class PaymentBaseModel(BaseModel):
    message: str
    balance: float
    name: str
    price: float


class PaymentMessageModel(BaseModel):
    message: str
