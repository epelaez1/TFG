from fastapi import APIRouter
from fastapi import Depends
from fastapi import status
from fastapi.security import OAuth2PasswordBearer
from fastapi.security import OAuth2PasswordRequestForm

from src.config import environment
from src.dependencies import user_repository
from src.user import user_services
from src.user.entrypoints import user_models as models

router: APIRouter = APIRouter(
    prefix='/user',
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/user/login')


async def get_current_user_email(token: str = Depends(oauth2_scheme)) -> str:
    return user_services.get_email_from_token(token=token, secret_key=environment.secret_key)


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    response_model=models.PublicUserData,
    name='user:register',
)
async def create_user(user: models.NewUser) -> dict[str, str | bool]:
    new_user = user_services.register_user(**user.dict(), user_repository=user_repository)
    return new_user.dict()


@router.post(
    '/login',
    status_code=status.HTTP_200_OK,
    response_model=models.Token,
    name='user:login',
)
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> dict[str, str]:
    user_token = user_services.login(
        email=form_data.username,
        password=form_data.password,
        user_repository=user_repository,
        secret_key=environment.secret_key,
    )
    return user_token.dict()


@router.get(
    '/',
    status_code=status.HTTP_200_OK,
    response_model=models.PublicUserData,
    name='user:my-user',
)
async def get_current_user(user_email: str = Depends(get_current_user_email)) -> dict[str, str | bool]:
    return user_services.get_user(email=user_email, user_repository=user_repository).dict()
