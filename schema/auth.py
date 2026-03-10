from pydantic import BaseModel


class AuthModel(BaseModel):
    access_token: str


class ErrorAuthModel(BaseModel):
    description: str
    error: str
    status_code: int
