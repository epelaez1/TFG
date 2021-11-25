from pydantic import BaseModel
from pydantic import EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str


class Credentials(BaseModel):
    email: EmailStr
    password: str
