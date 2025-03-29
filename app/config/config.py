from pydantic import SecretStr, PrivateAttr, BaseModel
from pydantic_settings import BaseSettings

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine


class PostgresConfig(BaseModel):
    _engine: Engine | None = PrivateAttr(default=None)

    connection_string: str

    @property
    def engine(self) -> Engine:
        if not self._engine:
            self._engine = create_engine(self.connection_string)
        return self._engine


class Config(BaseSettings):
    postgres: PostgresConfig
    SECRET_KEY: SecretStr
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    API_ENDPOINT_BASE_URL: str
    RATE_LIMIT_WINDOW: int
