
from litestar.exceptions import HTTPException
from sqlalchemy.exc import (
    DatabaseError,
    DBAPIError,
    InvalidRequestError,
    NoResultFound,
    NoSuchTableError,
    OperationalError,
    ProgrammingError,
    SQLAlchemyError,
)

from domain.logger import logger
from domain.typing import Result

ERROR_MAPPINGS = {SQLAlchemyError: (500, "Internal Server Error: SQLAlchemyError"),
                  DatabaseError: (500, "Internal Server Error: DatabaseError"),
                  OperationalError: (500, "Internal Server Error: OperationalError"),
                  InvalidRequestError: (500, "Internal Server Error: InvalidRequestError"),
                  NoSuchTableError: (500, "Internal Server Error: NoSuchTableError"),
                  TimeoutError: (500, "Internal Server Error: TimeoutError"),
                  ConnectionError: (500, "Internal Server Error: ConnectionError"),
                  ProgrammingError: (500, "Internal Server Error: ProgrammingError"),
                  NoResultFound: (404, "Not Found"),
                  OSError: (500, "Internal Server Error: [Errno 10061] Connect call failed"),
                  DBAPIError: (500, "DataBase connection error: DBAPIError")}


class MixinHandle:
    @staticmethod
    async def handle_result(result: Result) -> Result.value:
        if result.error:
            error_type = type(result.error)
            if error_type in ERROR_MAPPINGS:
                code, message = ERROR_MAPPINGS[error_type]
                logger.error(f"{code}: {message}")
                raise HTTPException(detail=message, status_code=code)
            message = "Internal Server Error: The error is not described"
            logger.error(f"500: {message}")
            raise HTTPException(detail=message, status_code=500)
        return result.value
