from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from dtos import ResponseWrapper
from exceptions import (
    CannotDeleteResourceException,
    CannotUpdateResourceException,
    ConflictWithExistingResourcesException,
    ResourceNotFoundException
)
from utils.constants import UNEXPECTED_ERROR


def resource_not_found_exception_handler(_request: Request, exc: ResourceNotFoundException):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content=ResponseWrapper(
            success=False,
            status_code=status.HTTP_404_NOT_FOUND,
            message=str(exc),
            data=None
        ).model_dump()
    )

def conflict_exception_handler(_request: Request, exc: ConflictWithExistingResourcesException):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content=ResponseWrapper(
            success=False,
            status_code=status.HTTP_409_CONFLICT,
            message=str(exc),
            data=None
        ).model_dump()
    )

def validation_exception_handler(_request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=ResponseWrapper(
            success=False,
            status_code=status.HTTP_400_BAD_REQUEST,
            message=str(exc),
            data=None
        ).model_dump()
    )

def cannot_update_exception_handler(_request: Request, exc: CannotUpdateResourceException):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=ResponseWrapper(
            success=False,
            status_code=status.HTTP_400_BAD_REQUEST,
            message=str(exc),
            data=None
        ).model_dump()
    )

def cannot_delete_exception_handler(_request: Request, exc: CannotDeleteResourceException):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=ResponseWrapper(
            success=False,
            status_code=status.HTTP_400_BAD_REQUEST,
            message=str(exc),
            data=None
        ).model_dump()
    )

def generic_exception_handler(_request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ResponseWrapper(
            success=False,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=UNEXPECTED_ERROR + str(exc),
            data=None
        ).model_dump()
    )