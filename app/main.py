from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from slowapi.errors import RateLimitExceeded


from app.common.exception.exceptions import (
    CustomError,
    handle_custom_error,
    handle_validation_error,
    handle_rate_limit_exceeded_error,
)

from app.routes import auth, f1api, root
from app.routes.root import limiter

import app.common.logging as custom_logging

from os import getenv
import google.cloud.logging


if (env := getenv("ENV")) and env == "prod":
    client = google.cloud.logging.Client()
    client.setup_logging()

app = FastAPI()


app.exception_handler(RateLimitExceeded)(handle_rate_limit_exceeded_error)

app.exception_handler(CustomError)(handle_custom_error)
app.exception_handler(RequestValidationError)(handle_validation_error)

app.include_router(auth.router)
app.include_router(root.router, prefix="", tags=["root"])
app.include_router(f1api.router)


@app.on_event("startup")
async def connect():
    custom_logging.init()
    app.state.limiter = limiter
