import sys
import logging

from loguru import logger


class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord):
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


def init():
    for name in logging.root.manager.loggerDict:
        logging.getLogger(name).handlers = []

    logging.getLogger("uvicorn").handlers = [InterceptHandler()]
    logging.getLogger("uvicorn.access").handlers = [InterceptHandler()]

    logger.configure(
        handlers=[
            {
                "sink": sys.stdout,
                "level": logging.DEBUG,  # minimum level of logs that should be intercepted
            }
        ]
    )
