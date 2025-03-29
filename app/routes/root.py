from http import HTTPStatus

from fastapi import APIRouter, Request

from slowapi import Limiter
from slowapi.util import get_remote_address

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)

HEALTH_DESCRIPTION = "Check to make sure the service is up and running"


@router.get(
    "/health",
    summary="Health check",
    status_code=HTTPStatus.OK,
    description=HEALTH_DESCRIPTION,
)
@limiter.limit("5/minute")
async def health(request: Request) -> None:
    """Simply returns with positive code if service is running as expected"""
    pass
