from typing import Any, Dict, Optional, Union

from app.config import config
from app.common.exception.exceptions import CustomError

from loguru import logger
from sqlalchemy.sql import text


def pgsql_query(sql: str, params: dict = None) -> list[dict]:
    engine = config.postgres.engine
    conn = None
    try:
        conn = engine.connect()
        logger.info("Connected to the PostgreSQL database.")

        result = conn.execute(text(sql), params or {})
        logger.info("Query executed successfully.")

        rows = result.fetchall()
        logger.info("Fetched all rows.")
        print("Fetched all rows.")

        columns = result.keys()
        result_list = [dict(zip(columns, row)) for row in rows]
        logger.info("Converted rows to a list of dictionaries.")
        print(f"Converted rows to a list of dictionaries. {result_list}")
    except Exception as e:
        logger.error(f"Error executing query: {e}")
        raise CustomError(f"Error executing query: {e}")
    finally:
        if conn is not None:
            conn.close()
            logger.info("Database connection closed.")
    return result_list


def get_pgql_data(
    query: str,
    params: Dict[str, Any],
    result_key: Optional[str] = None,
    log_message: str = "",
) -> Union[dict, str]:
    result = pgsql_query(query, params)
    if result:
        logger.info(f"{log_message} return: {result[0]}")
        return result[0][result_key] if result_key else result[0]
    return "" if result_key else {}


def get_client_by_id(client_id: str) -> dict:
    query = "SELECT * FROM client_scopes_get WHERE client_id = :client_id"
    return get_pgql_data(
        query=query, params={"client_id": client_id}, log_message="get_client_by_id"
    )


def get_client_scopes(client_id: str) -> str:
    query = "SELECT scopes FROM client_scopes_get WHERE client_id = :client_id"
    return get_pgql_data(
        query=query,
        params={"client_id": client_id},
        result_key="scopes",
        log_message="get_client_scopes",
    )
