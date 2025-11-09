from fastapi import FastAPI

def register_exception_handlers(app: FastAPI):
    from config.global_exception_handler import (
        resource_not_found_exception_handler,
        conflict_exception_handler,
        cannot_update_exception_handler,
        cannot_delete_exception_handler,
        generic_exception_handler
    )
    from exceptions.cannot_delete_resource_exception import CannotDeleteResourceException
    from exceptions.cannot_update_resource_exception import CannotUpdateResourceException
    from exceptions.conflict_with_existing_resources_exception import ConflictWithExistingResourcesException
    from exceptions.resource_not_found_exception import ResourceNotFoundException

    app.add_exception_handler(ResourceNotFoundException, resource_not_found_exception_handler)
    app.add_exception_handler(ConflictWithExistingResourcesException, conflict_exception_handler)
    app.add_exception_handler(CannotUpdateResourceException, cannot_update_exception_handler)
    app.add_exception_handler(CannotDeleteResourceException, cannot_delete_exception_handler)
    app.add_exception_handler(Exception, generic_exception_handler)