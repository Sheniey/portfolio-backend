
from typing import Optional
from fastapi import status

from app.core.errors import AppException
from app.core.models import AppResponse

# ╔══════════════════════════════╗ #
# ║        CUSTOM ERRORS         ║ #
# ╚══════════════════════════════╝ #
class InvalidSkillname(AppException):
    def __init__(self, skillname: str, path: Optional[str] = None, *, status_code: int = status.HTTP_400_BAD_REQUEST) -> None:
        super().__init__(
            model=AppResponse(
                success = False,
                error   = 'SKILL_NOT_FOUND',
                message = f'The specified skill [/{skillname}] was not found in the database.',
                meta    = AppResponse.MetaData(path=path)
            ),
            status_code=status_code
        )
