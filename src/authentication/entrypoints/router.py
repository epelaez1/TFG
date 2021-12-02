from fastapi import APIRouter
from fastapi import Depends
from fastapi import status
from fastapi.security import OAuth2PasswordRequestForm

from src.authentication import services
from src.authentication.domain.entities.session import SessionToken
from src.authentication.entrypoints import models
from src.config import environment
from src.dependencies import repositories


auth_router: APIRouter = APIRouter(
    prefix='/auth',
)


@auth_router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    name='auth:register',
    response_model=models.Token,
)
async def create_user(
    credentials: models.Credentials,
) -> SessionToken:
    return services.register_user(
        **credentials.dict(),
        credentials_repository=repositories.credentials_repository,
        secret_key=environment.secret_key,
    )


@auth_router.post(
    '/login',
    status_code=status.HTTP_200_OK,
    response_model=models.Token,
    name='auth:login',
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> SessionToken:
    return services.login(
        email=form_data.username,
        password=form_data.password,
        credentials_repository=repositories.credentials_repository,
        secret_key=environment.secret_key,
    )
