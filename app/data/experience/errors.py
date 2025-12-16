
from typing import Any, Optional
from fastapi import status

from app.core.errors import AppException
from app.core.models import AppResponse
from app.data.experience.types import experience_t

# ╔══════════════════════════════╗ #
# ║        CUSTOM ERRORS         ║ #
# ╚══════════════════════════════╝ #
class InvalidExperienceObject(AppException):
    def __init__(self, object_: Any, path: Optional[str] = None, *, status_code: int = status.HTTP_409_CONFLICT) -> None:
        self.__object: experience_t | Any | None = object_
        
        super().__init__(
            model=AppResponse(
                success = False,
                error   = 'INVALID_EXPERIENCE',
                message = 'The Experience date is invalid, wrong, or missing.',
                meta    = AppResponse.MetaData(path=path)
            ),
            status_code=status_code
        )
    
    def get_object(self) -> experience_t | None: return self.__object

class CompanyNameNotFound(AppException):
    def __init__(self, company: str, path: Optional[str] = None, *, status_code: int = status.HTTP_404_NOT_FOUND) -> None:
        self.__company: str = company
        
        super().__init__(
            model=AppResponse(
                success = False,
                error   = 'COMPANY_NOT_FOUND',
                message = f'No experience found for company name: {company}.',
                meta    = AppResponse.MetaData(path=path)
            ),
            status_code=status_code
        )
    
    def get_company(self) -> str: return self.__company
