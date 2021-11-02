from fastapi import FastAPI
from src.service_info.entrypoints import service_info_router


app = FastAPI()
app.include_router(service_info_router.router)

if __name__ == '__main__':
    print('Hello World')
