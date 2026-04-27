from pydantic import BaseModel, Field
from tools.fakers import fake


class UserBalanceModel(BaseModel):
    message: str
    balance: int


class BalancePayloads(BaseModel):
    balance: int = Field(default_factory=fake.user_balance)


class LowBalancePayloads(BaseModel):
    balance: int = Field(default_factory=fake.low_balance)


class BalanceMessageModel(BaseModel):
    message: str
