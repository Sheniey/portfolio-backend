
from typing import Final as Const
from fastapi import APIRouter, status, Response, Request, Path, Query

from app.core.models import AppResponse
from app.core.consts import DEFAULT_LANGUAGE
from app.utils import security
from app.utils.protection import rate_limiter
from app.data.skills.consts import METHODS_AVAILABLE
from app.data.skills import models, services

PATH: Const[str] = '/skills'
router: APIRouter = APIRouter(prefix=PATH, tags=['skills'])

# ╔══════════════════════════════╗ #
# ║       SKILL ENDPOINTS        ║ #
# ╚══════════════════════════════╝ #
@router.options(
    '/',
    response_class=Response,
    status_code=status.HTTP_204_NO_CONTENT,
    description='Returns the available methods for the /skills endpoint.'
)
@rate_limiter(60, 'minute')
async def options_skills(request: Request) -> Response:
    '''
    OPTIONS /skills\n
    Content-Type: none\n
    <br>
    Returns the available methods for the /skills endpoint.
    '''
    
    return Response(
        headers={
            'Allow': METHODS_AVAILABLE
        },
        status_code=status.HTTP_204_NO_CONTENT
    )



@router.get(
    '/',
    response_model=AppResponse[list[models.SkillOut]],
    status_code=status.HTTP_200_OK,
    description='Retrieve a list of all skills.'
)
@rate_limiter(120, 'minute')
async def get_skills(
        request: Request,
        lang: str = Query(
            DEFAULT_LANGUAGE,
            description='Language code for skill descriptions.'
        )
    ) -> AppResponse[list[models.SkillOut]]:
    '''
    GET /skills\n
    Content-type: application/json\n
    <br>
    Retrieve a list of all skills.
    '''
    
    payload: list[models.SkillOut] = services.fetch_all_skills(lang)
    return AppResponse(
        success=True,
        error=None,
        message='List of all skills retrieved successfully.',
        data=payload,
        meta=AppResponse.MetaData(path=PATH)
    )

@router.get(
    '/{skillname}',
    response_model=AppResponse[models.SkillOut],
    status_code=status.HTTP_200_OK,
    description='Retrieve information about a specific skill.'
)
@rate_limiter(120, 'minute')
async def get_skill(
        request: Request,
        skillname: str = Path(
            ...,
            description='The name of the skill to retrieve information for.'
        ),
        lang: str = Query(
            DEFAULT_LANGUAGE,
            description='Language code for skill description.'
        )
    ) -> AppResponse[models.SkillOut]:
    '''
    GET /skills/{skillname}\n
    Content-type: application/json\n
    <br>
    Retrieve information about a specific skill.
    '''
    __curr_path__: Const[str] = f'{PATH}/{skillname}'
    
    payload: models.SkillOut = services.fetch_skill_info(skillname, lang, path=__curr_path__)
    return AppResponse(
        success=True,
        error=None,
        message=f'Information for skill [/{skillname}] retrieved successfully.',
        data=payload,
        meta=AppResponse.MetaData(path=__curr_path__)
    )



@router.put(
    '/{skillname}',
    response_model=AppResponse,
    status_code=status.HTTP_200_OK,
    description='Update the information of a specific skill.'
)
@security.required_permissions(security.PERMITS.MAINTAINER)
@rate_limiter(60, 'minute')
async def update_skill_info(
        request: Request,
        body: models.SkillPatch,
        skillname: str = Path(
            ...,
            description='The name of the skill to update.'
        )
    ) -> AppResponse:
    '''
    PUT /skills/{skillname}\n
    Content-type: application/json\n
    <br>
    Update the information of a specific skill.
    '''
    __curr_path__: Const[str] = f'{PATH}/{skillname}'
    
    payload: None = services.update_skill(skillname, body, path=__curr_path__)
    return AppResponse(
        success=True,
        error=None,
        message = f'Skill [/{skillname}] has been successfully updated.',
        data=payload,
        meta=AppResponse.MetaData(path=__curr_path__)
    )



@router.patch(
    '/{skillname}',
    response_model=AppResponse,
    status_code=status.HTTP_200_OK,
    description='Update the information of a specific skill.'
)
@security.required_permissions(security.PERMITS.MAINTAINER)
@rate_limiter(30, 'minute')
async def edit_skill_info(
        request: Request,
        body: models.SkillIn,
        skillname: str = Path(
            ...,
            description='The name of the skill to update.'
        )
    ) -> AppResponse:
    '''
    PATCH /skills/{skillname}\n
    Content-type: application/json\n
    <br>
    Update the information of a specific skill.
    '''
    __curr_path__: Const[str] = f'{PATH}/{skillname}'
    
    payload: None = services.patch_skill(skillname, body, path=__curr_path__)
    return AppResponse(
        success=True,
        error=None,
        message = f'Skill [/{skillname}] has been successfully updated.',
        data=payload,
        meta=AppResponse.MetaData(path=__curr_path__)
    )

@router.delete(
    '/{skillname}',
    response_model=AppResponse,
    status_code=status.HTTP_200_OK,
    description='Delete a specific skill.'
)
@security.required_permissions(security.PERMITS.OWNER)
@rate_limiter(10, 'minute')
async def delete_skill(
        request: Request,
        skillname: str = Path(
            ...,
            description='The name of the skill to delete.'
        )
    ) -> AppResponse:
    '''
    DELETE /skills/{skillname}\n
    Content-type: application/json\n
    <br>
    Delete a specific skill.
    '''
    __curr_path__: Const[str] = f'{PATH}/{skillname}'
    
    payload: None = services.delete_skill(skillname, path=__curr_path__)
    return AppResponse(
        success=True,
        error=None,
        message = f'Skill [/{skillname}] has been successfully deleted.',
        data=payload,
        meta=AppResponse.MetaData(path=__curr_path__)
    )
