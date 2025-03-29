FROM python:3.11-slim

WORKDIR /usr/src

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_VERSION=0.4.0

ENV PATH="/root/.local/bin:$PATH"

RUN pip install pipx
RUN pipx install uv==${UV_VERSION}


COPY ./uv.lock pyproject.toml /usr/src/

COPY app /usr/src/app

CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]