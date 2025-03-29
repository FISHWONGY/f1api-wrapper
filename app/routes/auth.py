from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, Request
from jose import jwt

from loguru import logger

from app.config import config
from app.schema.auth import TokenResponse, TokenRequestForm

from app.common.gcp_cloudsql import get_client_by_id
from app.common.exception.exceptions import UnauthorizedException

from app.routes.root import limiter


router = APIRouter(prefix="/auth", tags=["auth"])


def authenticate_client(client_id: str, client_secret: str):
    client = get_client_by_id(client_id)
    if client and client["client_secret"] == client_secret and client["is_active"] == 1:
        return client
    return None


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, config.SECRET_KEY.get_secret_value(), algorithm=config.ALGORITHM
    )
    return encoded_jwt


@router.post("/token", response_model=TokenResponse)
@limiter.limit("5/minute")
async def login_for_access_token(
    request: Request, form_data: TokenRequestForm = Depends()
):
    client = authenticate_client(form_data.client_id, form_data.client_secret)
    if not client:
        logger.error("Invalid client ID or secret")
        raise UnauthorizedException("Invalid client ID or secret")

    access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": client["client_id"]}, expires_delta=access_token_expires
    )
    logger.info("Access token created successfully")
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=60 * config.ACCESS_TOKEN_EXPIRE_MINUTES,
    )
