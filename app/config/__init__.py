from app.config.config import Config, PostgresConfig
from app.common.gcp_secrets import GCPSecrets

from os import getenv

secrets = GCPSecrets()

if (env := getenv("ENV")) and env == "prod":
    api_endpoint_base_url = secrets.get_secret("f1api-wrapper-endpoint")
else:
    api_endpoint_base_url = "http://127.0.0.1:8000"


config = Config(
    postgres=PostgresConfig(
        connection_string=secrets.get_secret("f1api-pgsql-conn-str"),
    ),
    SECRET_KEY=secrets.get_secret("f1api-wrapper-secret-key"),
    ALGORITHM="HS256",
    ACCESS_TOKEN_EXPIRE_MINUTES=180,
    API_ENDPOINT_BASE_URL=api_endpoint_base_url,
    RATE_LIMIT_WINDOW=60,
)
