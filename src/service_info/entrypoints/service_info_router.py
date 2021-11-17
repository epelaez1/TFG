from fastapi import APIRouter
from fastapi import status

router: APIRouter = APIRouter(
    prefix='/service_info',
)


@router.get(
    '/',
    status_code=status.HTTP_200_OK,
    name='service-info',
)
async def get_service_status() -> dict[str, str]:
    return {'status': 'ok'}
