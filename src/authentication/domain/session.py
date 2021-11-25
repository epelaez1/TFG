import json
from datetime import datetime
from datetime import timedelta
from typing import Any

from jose import ExpiredSignatureError
from jose import jwt
from jose import JWTError
from pydantic import BaseModel

from src.authentication.domain.exceptions import Unauthorized


class SessionToken(BaseModel):
    access_token: str
    token_type: str = 'bearer'

    def decode_payload(self, secret_key: str) -> Any:
        payload: dict[str, str]
        try:
            payload = jwt.decode(self.access_token, secret_key, algorithms=['HS256'])
        except (JWTError, ExpiredSignatureError) as jwt_error:
            raise Unauthorized() from jwt_error
        try:
            return json.loads(payload['sub'])
        except (KeyError, json.decoder.JSONDecodeError) as json_error:
            raise Unauthorized() from json_error


def create_session_token(token_info: dict[str, Any], duration: timedelta, secret_key: str) -> SessionToken:
    expire = datetime.utcnow() + duration
    to_encode = {'sub': json.dumps(token_info), 'exp': expire}
    return SessionToken(access_token=jwt.encode(to_encode, secret_key, algorithm='HS256'))
