import traceback

from fastapi import HTTPException, Request, status
from fastapi.exception_handlers import http_exception_handler
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException


class APIException(HTTPException):
    """
    Base API exception with a default status code and detail.
    """

    def __init__(
        self,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        detail: str = "An error occurred",
        headers: dict | None = None,
    ):
        super().__init__(status_code=status_code, detail=detail, headers=headers)


class UnauthorizedException(APIException):
    def __init__(self, detail: str = "Unauthorized"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)


class ForbiddenException(APIException):
    def __init__(self, detail: str = "Forbidden"):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)


class NotFoundException(APIException):
    def __init__(self, detail: str = "Resource not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class InternalServerException(APIException):
    def __init__(self, detail: str = "Internal Server Error"):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)


async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
    # Do a traceback
    traceback.print_exc()
    return await http_exception_handler(request, exc)


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    print(f"Validation error: {exc}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors(), "body": exc.body},
    )
