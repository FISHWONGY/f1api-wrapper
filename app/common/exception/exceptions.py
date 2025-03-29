from http import HTTPStatus
from typing import Any, Sequence

from fastapi import Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel

from starlette.responses import JSONResponse

from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler

from app.config import config


class ErrorResponse(BaseModel):
    cause: str
    detail: Any | None = None
    message: str | None = None


class ValidationErrorResponse(ErrorResponse):
    detail: Sequence[Any]


class CustomError(RuntimeError):
    def __init__(
        self, message: str, response_code: int = 500, human_message: str | None = None
    ):
        self.response_code = response_code
        self.message = message
        self.human_message = human_message
        super().__init__(message)

    def to_response(self) -> ErrorResponse:
        return ErrorResponse(cause=self.message, message=self.human_message).model_dump(
            mode="json", exclude_none=True
        )


def handle_custom_error(req: Request, exc: CustomError):
    return JSONResponse(exc.to_response(), status_code=exc.response_code)


def handle_validation_error(req: Request, exc: RequestValidationError):
    return JSONResponse(
        ErrorResponse(
            cause="Request data validation error",
            detail=jsonable_encoder(exc.errors()),
            message="Invalid data was sent to the server",
        ).model_dump(mode="json"),
        status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
    )


def handle_rate_limit_exceeded_error(request: Request, exc: RateLimitExceeded):
    response = _rate_limit_exceeded_handler(request, exc)
    response.headers["Retry-After"] = str(config.RATE_LIMIT_WINDOW)
    return response


class UnauthorizedException(CustomError):
    def __init__(self, message: str | None = None):
        super().__init__(
            "Unauthorized", response_code=HTTPStatus.UNAUTHORIZED, human_message=message
        )


class NotFound(CustomError):
    def __init__(self, message: str | None = None):
        super().__init__(
            "Item not found", response_code=HTTPStatus.NOT_FOUND, human_message=message
        )


class BadRequest(CustomError):
    def __init__(self, message: str | None = None):
        super().__init__(
            "Bad request", response_code=HTTPStatus.BAD_REQUEST, human_message=message
        )
