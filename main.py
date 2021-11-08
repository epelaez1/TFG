from fastapi import FastAPI

from src.service_info.entrypoints import service_info_router
from src.user.entrypoints import user_router

app = FastAPI()
app.include_router(service_info_router.router)
app.include_router(user_router.router)
