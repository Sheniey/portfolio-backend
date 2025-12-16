
from typing import Any, Optional
from fastapi import status

from app.core.errors import AppException
from app.core.models import AppResponse
from app.data.projects.models import ProjectIn
from app.data.projects.types import project_t

# ╔══════════════════════════════╗ #
# ║        CUSTOM ERRORS         ║ #
# ╚══════════════════════════════╝ #
class InvalidProjectId(AppException):
    def __init__(self, id: int, path: Optional[str] = None,  *, status_code: int = status.HTTP_400_BAD_REQUEST) -> None:
        self.__id: int = id
        
        super().__init__(
            model=AppResponse(
                success = False,
                error   = 'INVALID_PROJECT_ID',
                message = f'The project id [/{id}] not found in projects.',
                meta    = AppResponse.MetaData(path=path)
            ),
            status_code=status_code
        )
    
    def get_id(self) -> int | Any: return self.__id

class InvalidProjectType(AppException):
    def __init__(self, type_project: str, path: Optional[str] = None,  *, status_code: int = status.HTTP_400_BAD_REQUEST) -> None:
        self.__type: int = type_project
        
        super().__init__(
            model=AppResponse(
                success = False,
                error   = 'INVALID_REQUEST',
                message = f"The builder project [{type_project}] isn't exist.",
                meta    = AppResponse.MetaData(path=path)
            ),
            status_code=status_code
        )
    
    def get_type(self) -> int | Any: return self.__type
    
class InvalidProjectObject(AppException):
    def __init__(self, object_: Any, path: Optional[str] = None,  *, status_code: int = status.HTTP_409_CONFLICT) -> None:
        self.__object: project_t | Any | None = object_
        message: str = 'The Project object is invalid.'
        
        super().__init__(
            model=AppResponse(
                success = False,
                error   = 'INVALID_PROJECT',
                message = message,
                meta    = AppResponse.MetaData(path=path)
            ),
            status_code=status_code
        )
    
    def __init__(self, object_: Any, path: Optional[str] = None,  *, status_code: int = status.HTTP_409_CONFLICT) -> None:
        self.__object: project_t | Any | None = object_
        
        message: str
        if not isinstance(object_, dict) or not isinstance(object_, ProjectIn):
            message = "The object isn't a valid Project instance."
        else:
            message = f'Some required attributes are missing.'
        
        super().__init__(
            model=AppResponse(
                success = False,
                error   = 'INVALID_PROJECT',
                message = message,
                meta    = AppResponse.MetaData(path=path)
            ),
            status_code=status_code
        )
    
    def get_object(self) -> dict | None: return self.__object

class ConfirmRequiredAction(AppException):
    def __init__(self, path: Optional[str] = None, *, status_code: int = status.HTTP_400_BAD_REQUEST) -> None:
        super().__init__(
            model=AppResponse(
                success = False,
                error   = 'CONFIRM_REQUIRED',
                message = f'Require confirm in "{path}?confirm=true".',
                meta    = AppResponse.MetaData(path=path)
            ),
            status_code=status_code
        )
