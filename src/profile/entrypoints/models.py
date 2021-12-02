from pydantic import BaseModel


class BaseProfile(BaseModel):
    name: str
    phone: str


class PublicProfile(BaseProfile):
    email: str


class Token(BaseModel):
    access_token: str
    token_type: str
