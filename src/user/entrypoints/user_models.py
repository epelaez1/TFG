from pydantic import BaseModel
from pydantic import EmailStr


class BaseUser(BaseModel):
    name: str
    email: EmailStr
    phone: str


class NewUser(BaseUser):
    password: str


class PublicUserData(BaseUser):
    verified: bool


class Token(BaseModel):
    access_token: str
    token_type: str
