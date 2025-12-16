
from typing import Final as Const
from fastapi import APIRouter, Path, Query, status, Response, Request

from app.core.models import AppResponse
from app.core.types import Language
from app.core.consts import DEFAULT_LANGUAGE
from app.utils import security
from app.utils.protection import rate_limiter
from app.data.experience.consts import METHODS_AVAILABLE
from app.data.experience import services, models

PATH: Const = '/experiences'
router: APIRouter = APIRouter(prefix=PATH, tags=['my-experience'])

# ╔══════════════════════════════╗ #
# ║   MY EXPERIENCE ENDPOINTS    ║ #
# ╚══════════════════════════════╝ #
@router.options(
    '/',
    response_class=Response,
    status_code=status.HTTP_204_NO_CONTENT,
)
@rate_limiter(60, 'minute')
async def experiences_options(request: Request) -> Response:
    '''
    OPTIONS /experiences\n
    Content-Type: none\n
    <br>
    Return experience endpoint methods.
    '''
    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
        headers={
            'Allow': METHODS_AVAILABLE
        }
    )



@router.get(
    '/',
    response_model=AppResponse[list[models.ExperienceOut]],
    status_code=status.HTTP_200_OK,
    description='Retrieve all experiences.',
)
@rate_limiter(120, 'minute')
async def get_all_experiences(
        request: Request,
        lang: Language = Query(DEFAULT_LANGUAGE, description='Language code for localization.')
    ) -> AppResponse[list[models.ExperienceOut]]:
    '''
    GET /experiences\n
    Content-Type: application/json\n
    <br>
    Retrieve all experiences.
    '''
    
    payload: list[models.ExperienceOut] = services.get_experience_list(lang, path=PATH)
    return AppResponse(
        success=True,
        error=None,
        message='Experiences retrieved successfully.',
        data=payload,
        meta=AppResponse.MetaData(path=PATH)
    )

@router.get(
    '/{company}',
    response_model=AppResponse[list[models.ExperienceOut]],
    status_code=status.HTTP_200_OK,
    description='Retrieve experiences by company name.',
)
@rate_limiter(120, 'minute')
async def get_experiences_for_company(
        request: Request,
        company: str = Path(..., description='Name of the company to filter experiences.'),
        lang: Language = Query(DEFAULT_LANGUAGE, description='Language code for localization.')
    ) -> AppResponse[list[models.ExperienceOut]]:
    '''
    GET /experiences/{company}\n
    Content-Type: application/json\n
    <br>
    Retrieve experiences for a specific company.
    '''
    
    payload: list[models.ExperienceOut] = services.get_experiences_by_company(company, lang, path=PATH)
    return AppResponse(
        success=True,
        error=None,
        message=f'Experiences for company "{company}" retrieved successfully.',
        data=payload,
        meta=AppResponse.MetaData(path=PATH)
    )



@router.put(
    '/',
    response_model=AppResponse[models.PostContentResponse],
    status_code=status.HTTP_201_CREATED,
    description='Create a new experience entry.',
)
@security.required_permissions(security.PERMITS.OWNER)
@rate_limiter(30, 'minute')
async def create_experience(
        request: Request,
        body: models.ExperienceIn
    ) -> AppResponse[models.PostContentResponse]:
    '''
    PUT /experiences\n
    Content-Type: application/json\n
    <br>
    Create a new experience entry.
    '''
    
    payload: models.PostContentResponse = services.make_new_experience(body, path=PATH)
    return AppResponse(
        success=True,
        error=None,
        message='Experience created successfully.',
        data=payload,
        meta=AppResponse.MetaData(path=PATH)
    )



@router.delete(
    '/',
    response_model=AppResponse,
    status_code=status.HTTP_200_OK, 
    description='Delete an experience by its ID.',
)
@security.required_permissions(security.PERMITS.OWNER)
@rate_limiter(10, 'minute')
async def delete_experiences_by_company(
        request: Request,
        company: str = Path(..., description='Name of the company whose experiences to delete.')
    ) -> AppResponse:
    '''
    DELETE /experiences/{company}\n
    Content-Type: application/json\n
    <br>
    Delete all experiences for a specific company.
    '''
    
    len_before: int = services.sizeof_db()
    services.delete_experiences_by_company(company, path=PATH)
    len_after: int = services.sizeof_db()
    
    return AppResponse(
        success=True,
        error=None,
        message=f'{len_before - len_after} of my Experiences were successfully deleted.',
        data=None,
        meta=AppResponse.MetaData(path=PATH)
    )
