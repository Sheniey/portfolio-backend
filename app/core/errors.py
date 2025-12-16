
from typing import Self, Optional
from fastapi import status, HTTPException

from app.core.consts import SUPPORTED_LANGUAGES, DEFAULT_LANGUAGE
from app.core.types import Language
from app.core.models import AppResponse

# ╔══════════════════════════════╗ #
# ║      PATTERN EXCEPTIONS      ║ #
# ╚══════════════════════════════╝ #
class AppException(Exception):
    def __init__(self, model: AppResponse, *, status_code: int = status.HTTP_400_BAD_REQUEST) -> None:
        self.__status_code: int = status_code
        
        model.success = False
        model.error = model.error.upper().replace(' ', '_')
        self.__model: AppResponse = model
        
        self.__prompt: str = f'''
 [!] {self.__model.error}: | {self.__model.message} |...
{f'  └── [*] On: [{self.__model.meta.path}]' if self.__model.meta.path else ''}
'''
        super().__init__(self.__prompt)
    
    def get_status_code(self) -> int:
        return self.__status_code
    
    def get_model(self) -> AppResponse:
        return self.__model.model_dump()
    
    def log(self) -> Self:
        print(self.__prompt)
        return self 
    
    def log_json(self) -> Self:
        print(self.__model.model_dump_json())
        return self
    
    def throw(self) -> HTTPException:
        return HTTPException(self.__status_code, self.__model.model_dump())


# ╔══════════════════════════════╗ #
# ║     DAUGHTER EXCEPTIONS      ║ #
# ╚══════════════════════════════╝ #
class Unauthenticated(AppException):
    def __init__(self,
        details: str = 'You must be authenticated to access this resource.',
        path: Optional[str] = None,
        *,
        status_code: int = status.HTTP_401_UNAUTHORIZED,
    ) -> None:
        super().__init__(
            model=AppResponse(
                success = False,
                error   = 'UNAUTHENTICATED',
                message = details,
                data    = None,
                meta    = AppResponse.MetaData(path=path)
            ),
            status_code=status_code,
        )

class Unauthorized(AppException):
    def __init__(self,
        details: str = 'Your current role does not have permission to access this resource.',
        path: Optional[str] = None,
        *,
        status_code: int = status.HTTP_403_FORBIDDEN,
    ) -> None:
        super().__init__(
            model=AppResponse(
                success = False,
                error   = 'UNAUTHORIZED',
                message = details,
                data    = None,
                meta    = AppResponse.MetaData(path=path)
            ),
            status_code=status_code,
        )

class TranslationNotAvailable(AppException):
    def __init__(self,
        element: dict[Language, str],
        requested_lang: Language,
        default_lang: Language = DEFAULT_LANGUAGE,
        path: Optional[str] = None,
        *,
        status_code: int = status.HTTP_501_NOT_IMPLEMENTED,
    ) -> None:
        super().__init__(
            model=AppResponse(
                success = False,
                error   = 'TRANSLATION_NOT_AVAILABLE',
                message = f'Translation not available for language: {requested_lang}.',
                data    = {
                    'requested_language': requested_lang,
                    'available_languages': list(element.keys()),
                    'expected_available_languages': SUPPORTED_LANGUAGES,
                    'default_language': default_lang,
                    'default_translation': element.get(default_lang, None),
                },
                meta    = AppResponse.MetaData(path=path)
            ),
            status_code=status_code,
        )
