from fastapi import FastAPI

from src.bootstrap import initialize_app


app: FastAPI = initialize_app()
