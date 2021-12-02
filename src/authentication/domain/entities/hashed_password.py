from passlib.context import CryptContext
from pydantic import BaseModel

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class HashedPassword(BaseModel):
    __root__: str

    def verify_password(self, plain_password: str) -> bool:
        return bool(pwd_context.verify(plain_password, self.__root__))


def hash_password(plain_password: str) -> HashedPassword:
    password_hash: str = pwd_context.hash(plain_password)
    return HashedPassword(__root__=password_hash)
