from fastapi import APIRouter
from fastapi import Depends
from fastapi import status

from src.authentication import services as auth_services
from src.authentication.domain.entities.session import SessionToken
from src.config import environment
from src.dependencies import authorized_user_email
from src.dependencies import profile_creation_email
from src.dependencies import repositories
from src.profile import services
from src.profile.domain.entities.profile import Profile
from src.profile.entrypoints import models

profile_router: APIRouter = APIRouter(
    prefix='/profile',
)


@profile_router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    response_model=models.Token,
    name='profile:register',
)
async def create_profile(
    profile: models.BaseProfile,
    email: str = Depends(profile_creation_email),
) -> SessionToken:
    services.register_profile(
        **profile.dict(),
        email=email,
        profile_repository=repositories.profile_repository,
    )
    return auth_services.update_profile(
        email=email,
        credentials_repository=repositories.credentials_repository,
        secret_key=environment.secret_key,
    )


@profile_router.get(
    '/',
    status_code=status.HTTP_200_OK,
    response_model=models.PublicProfile,
    name='profile:my-profile',
)
async def get_current_profile(
    profile_email: str = Depends(authorized_user_email),
) -> Profile:
    return services.get_profile(email=profile_email, profile_repository=repositories.profile_repository)
