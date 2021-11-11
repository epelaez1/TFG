from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import status
from pydantic import BaseModel
from pydantic import EmailStr

from src.bootstrap import user_repository
from src.user.domain.user_exceptions import UserAlreadyRegistered
from src.user.user_services import register_user

router: APIRouter = APIRouter(
    prefix='/user',
)


class NewUser(BaseModel):
    name: str
    email: EmailStr
    phone: str


class User(NewUser):
    verified: bool


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    response_model=User,
)
async def create_user(user: NewUser) -> dict[str, str | bool]:
    try:
        new_user = register_user(user_repository=user_repository, email=user.email, name=user.name, phone=user.phone)
    except UserAlreadyRegistered:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User already exists')
    return new_user.to_dict()
