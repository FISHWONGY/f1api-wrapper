from typing import Annotated

from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordBearer

from passlib.context import CryptContext
from jose import JWTError, jwt

from loguru import logger

from app.config import config
from app.schema.auth import TokenData
from app.common.exception.exceptions import UnauthorizedException

from app.common.gcp_cloudsql import get_client_scopes


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], request: Request
):
    try:
        payload = jwt.decode(
            token, config.SECRET_KEY.get_secret_value(), algorithms=[config.ALGORITHM]
        )
        client_id: str = payload.get("sub")
        if client_id is None:
            logger.error("Could not validate credentials, missing client id")
            raise UnauthorizedException("Could not validate credentials")

        scopes = get_client_scopes(client_id)
        logger.info(f"Client scopes: {scopes}")
        endpoint = request.url.path[1:]
        logger.info(f"Endpoint: {request.url.path}")

        if endpoint not in [scope.strip() for scope in scopes.split(",")]:
            logger.error(f"Client does not have access to endpoint: {endpoint}")
            raise UnauthorizedException("Client does not have access to this endpoint")

        token_data = TokenData(client_id=client_id)
    except JWTError as e:
        logger.error(f"JWTError, Could not validate credentials: {e}")
        raise UnauthorizedException("Could not validate credentials")
    return token_data
