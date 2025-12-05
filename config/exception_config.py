from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from config.global_exception_handler import validation_exception_handler

def register_exception_handlers(app: FastAPI):
    from config.global_exception_handler import (
        resource_not_found_exception_handler,
        conflict_exception_handler,
        cannot_update_exception_handler,
        cannot_delete_exception_handler,
        generic_exception_handler,
        invalid_argument_exception_handler
    )
    from exceptions import (
        CannotDeleteResourceException,
        CannotUpdateResourceException,
        ConflictWithExistingResourcesException,
        ResourceNotFoundException,
        InvalidArgumentException
    )

    app.add_exception_handler(ResourceNotFoundException, resource_not_found_exception_handler)
    app.add_exception_handler(ConflictWithExistingResourcesException, conflict_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(CannotUpdateResourceException, cannot_update_exception_handler)
    app.add_exception_handler(CannotDeleteResourceException, cannot_delete_exception_handler)
    app.add_exception_handler(Exception, generic_exception_handler)
    app.add_exception_handler(InvalidArgumentException, invalid_argument_exception_handler)