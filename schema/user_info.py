from pydantic import BaseModel, Field

from tools.fakers import fake


class Address(BaseModel):
    city: str = Field(default_factory=fake.city)
    street: str = Field(default_factory=fake.street)
    home_number: str = Field(default_factory=fake.home_number)


class AddUserInfoPayloads(BaseModel):
    phone: str = Field(default_factory=fake.phone)
    email: str = Field(default_factory=fake.email)
    address: Address = Address()


class UpdateUserInfoPayloads(BaseModel):
    phone: str = Field(default_factory=fake.phone)
    email: str = Field(default_factory=fake.email)
    address: Address = Address()


class UserInfoBaseModel(BaseModel):
    message: str


class GetUserInfoModel(BaseModel):
    city: str
    street: str
    userID: int
    phone: str
    email: str


class ErrorUserInfoModel(BaseModel):
    description: str
    error: str
    status_code: int
