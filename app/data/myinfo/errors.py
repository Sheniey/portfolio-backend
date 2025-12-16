
from typing import Optional
from fastapi import status

from app.core.errors import AppException
from app.core.models import AppResponse
from app.data.myinfo.types import myinfo_t

# ╔══════════════════════════════╗ #
# ║        CUSTOM ERRORS         ║ #
# ╚══════════════════════════════╝ #
class InfoNotFoundError(AppException):
    def __init__(self, path: Optional[str] = None, *, status_code = status.HTTP_500_INTERNAL_SERVER_ERROR) -> None:
        super().__init__(
            model=AppResponse(
                success=False,
                error='INFO_NOT_FOUND',
                message='Personal information not found in the database.',
                meta=AppResponse.MetaData(path=path)
            ),
            status_code=status_code
        )

class InvalidInfoObject(AppException):
    def __init__(self, info: object, path: Optional[str] = None, *, status_code = status.HTTP_400_BAD_REQUEST) -> None:
        super().__init__(
            model=AppResponse(
                success=False,
                error='INVALID_INFO_OBJECT',
                message=f'The provided personal information object is invalid: {info}',
                meta=AppResponse.MetaData(path=path)
            ),
            status_code=status_code
        )
    
class AttributeNotFound(AppException):
    __example_myinfo: myinfo_t = {
        'full_name': 'Example Name',
        'first_name': 'Example',
        'last_name': 'Name',
        'pseudonym': 'Example',
        'pseudonym_ascii': 'Example',
        'about_me': {
            'en': 'This is an example about me section in English.',
            'es': 'Esta es una sección de "sobre mí" de ejemplo en español.'
        },
        'phone': '1234567890',
        'email': 'example@example.com'
    }
    __attributes_myinfo: list[str] = list(__example_myinfo.keys())

    @classmethod
    def get_nearby_attributes(cls, expected_attr: str) -> str:
        def common_prefix(expected_value: str, value: str) -> int:
            length: int = 0
            for x, y in zip(expected_value, value):
                if x == y:
                    length += 1
                else:
                    break
            return length

        best_attr: Optional[str] = None
        best_score: int = 0
        score: int = 0

        for attr in cls.__attributes_myinfo:
            score = common_prefix(expected_attr, attr)
            if score > best_score:
                best_score = score
                best_attr = attr

        return best_attr if best_attr is not None else cls.__attributes_myinfo[0]
    
    def __init__(self, attr: str, path: Optional[str] = None, *, status_code = status.HTTP_400_BAD_REQUEST) -> None:
        suggestion: str = self.get_nearby_attributes(attr)
        
        super().__init__(
            model=AppResponse(
                success=False,
                error='INFO_NOT_FOUND',
                message=f'The attribute "{attr}" was not found in the personal information.',
                data={
                    'attribute': attr,
                    'suggestion': suggestion,
                    'available_attributes': self.__attributes_myinfo
                },
                meta=AppResponse.MetaData(path=path)
            ),
            status_code=status_code
        )
