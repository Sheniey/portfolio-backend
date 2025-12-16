
from typing import Final as Const
from fastapi import APIRouter, Request, status, Query, Response

from app.core.models import AppResponse
from app.core.types import Language
from app.core.consts import DEFAULT_LANGUAGE
from app.utils import security
from app.utils.protection import rate_limiter
from app.data.myinfo.consts import METHODS_AVAILABLE
from app.data.myinfo import services, models

PATH: Const[str] = '/personal-info'
router: APIRouter = APIRouter(prefix=PATH, tags=['personal-information'])

# ╔══════════════════════════════╗ #
# ║    MY OWN INFO ENDPOINTS     ║ #
# ╚══════════════════════════════╝ #
@router.options(
    '/',
    response_class=Response,
    status_code=status.HTTP_204_NO_CONTENT,
    description='Options for personal information endpoint.'
)
@rate_limiter(60, 'minute')
async def personal_info_options(request: Request) -> Response:
    '''
    OPTIONS /personal-info\n
    Content-Type: none\n
    <br>
    Return personal information endpoint methods.
    '''
    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
        headers={
            'Allow': METHODS_AVAILABLE
        }
    )


@router.get(
    '/',
    response_model=AppResponse[models.MyInfoOut],
    status_code=status.HTTP_200_OK,
    description='Get full personal information of the user.'
)
@rate_limiter(120, 'minute')
async def get_full_info(
        request: Request,
        lang: Language = Query(
            DEFAULT_LANGUAGE,
            description='Language for the personal information.'
        )
    ) -> AppResponse[models.MyInfoOut]:
    '''
    GET /personal-info\n
    Content-Type: application/json\n
    <br>
    Retrieve full personal information of the user.
    '''
    
    info: models.MyInfoOut = services.get_myinfo(lang, path=PATH)
    return AppResponse(
        success=True,
        error=None,
        message='Personal information retrieved successfully.',
        data=info,
        meta=AppResponse.MetaData(path=PATH)
    )


@router.put(
    '/',
    response_model=AppResponse,
    status_code=status.HTTP_202_ACCEPTED,
    description='Edit personal information of the user.'
)
@security.required_permissions(security.PERMITS.OWNER)
@rate_limiter(30, 'minute')
async def edit_full_info(
        request: Request,
        body: models.MyInfoIn
    ) -> AppResponse:
    '''
    PUT /personal-info\n
    Content-Type: application/json\n
    <br>
    Edit personal information of the user.
    '''
    
    services.edit_myinfo(body.model_dump(), path=PATH)
    return AppResponse(
        success=True,
        error=None,
        message='Personal information updated successfully.',
        data=None,
        meta=AppResponse.MetaData(path=PATH)
    )


@router.delete(
    '/',
    response_model=AppResponse,
    status_code=status.HTTP_200_OK,
    description='Delete all personal information of the user.'
)
@security.required_permissions(security.PERMITS.OWNER)
@rate_limiter(10, 'minute')
async def delete_full_info(request: Request) -> AppResponse:
    '''
    DELETE /personal-info\n
    Content-Type: application/json\n
    <br>
    Delete all personal information of the user.
    '''
    
    services.delete_everything(path=PATH)
    return AppResponse(
        success=True,
        error=None,
        message='All my personal information deleted successfully.',
        data=None,
        meta=AppResponse.MetaData(path=PATH)
    )
