from pydantic import BaseModel


class APIError(BaseModel):
    error_code: int
    detail: str
