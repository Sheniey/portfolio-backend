
from typing import Final as Const
from fastapi import APIRouter, status, Query, Path, Response, Request

from app.core.models import AppResponse
from app.core.consts import DEFAULT_LANGUAGE
from app.utils import security
from app.utils.protection import rate_limiter
from app.utils.i18n import Language
from app.data.projects.consts import METHODS_AVAILABLE
from app.data.projects import models, services

PATH: Const[str] = '/projects'
router: APIRouter = APIRouter(prefix=PATH, tags=['projects'])

# ╔══════════════════════════════╗ #
# ║      PROJECT ENDPOINTS       ║ #
# ╚══════════════════════════════╝ #
@router.options(
    '/',
    response_class=Response,
    status_code=status.HTTP_204_NO_CONTENT,
    description='Options for projects endpoint.'
)
@rate_limiter(60, 'minute')
async def projects_options(request: Request) -> Response:
    '''
    OPTIONS /projects\n
    Content-Type: none\n
    <br>
    Return projects endpoint methods.
    '''
    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
        headers={
            'Allow': METHODS_AVAILABLE
        }
    )



@router.get(
    '/',
    response_model=AppResponse[list[models.ProjectOut]],
    status_code=status.HTTP_200_OK,
    description='Get all projects.'
)
@rate_limiter(120, 'minute')
async def get_projects(
        request: Request,
        lang: Language = Query(
            DEFAULT_LANGUAGE,
            description='Language for the project data.'
        )
    ) -> AppResponse[list[models.ProjectOut]]:
    '''
    GET /projects\n
    Content-type: application/json\n
    <br>
    Get all projects.
    '''
    
    payload: list[models.ProjectOut] = services.load_projects(lang, path=PATH)
    response: AppResponse = AppResponse(
        success=True,
        error=None,
        message=f'{services.sizeof_db()} Projects were successfully obtained.',
        data=payload,
        meta=AppResponse.MetaData(path=PATH)
    )
    return response

# FastAPI, you bastard!
# Why won't it lemme create the Exception Handler so that Swagger doesn't throw up its stupid errors when it validates {id:int}?
# So... "id: str" ==> it's insane
@router.get(
    '/{id}',
    response_model=AppResponse[models.ProjectOut],
    status_code=status.HTTP_200_OK,
    description='Get a specific project by ID, name, or project_type.'
)
@rate_limiter(120, 'minute')
async def get_project(
        request: Request,
        id: str = Path(
            ...,
            description='ID, name, or project_type of the project to retrieve.'
        ),
        lang: Language = Query(
            DEFAULT_LANGUAGE,
            description='Language for the project data.'
        )
    ) -> AppResponse[models.ProjectOut]:
    '''
    GET /projects/{id}?lang={lang}\n
    Content-type: application/json\n
    <br>
    Get a specific project by ID, name, or project_type.
    '''
    __curr_path__: str = f'{PATH}/{id}'
    
    payload: models.ProjectOut = services.fetch_project(id, lang, path=__curr_path__)
    response: AppResponse[models.ProjectOut] = AppResponse(
        success=True,
        error=None,
        message='Project was successfully obtained.',
        data=payload,
        meta=AppResponse.MetaData(path=__curr_path__)
    )
    return response

@router.get(
    '/groups',
    response_model=AppResponse[list[models.ProjectGroupOut]],
    status_code=status.HTTP_200_OK,
)
@rate_limiter(40, 'minute')
async def get_project_groups(
        request: Request,
        lang: Language = Query(
            DEFAULT_LANGUAGE,
            description='Language for the project data.'
        )
    ) -> AppResponse[list[models.ProjectGroupOut]]:
    '''
    GET /projects/groups\n
    Content-type: application/json\n
    <br>
    Get all project groups.
    '''
    
    payload: list[models.ProjectGroupOut] = services.fetch_project_groups(lang, path=PATH)
    response: AppResponse[list[models.ProjectGroupOut]] = AppResponse(
        success=True,
        error=None,
        message='Project groups were successfully obtained.',
        data=payload,
        meta=AppResponse.MetaData(path=PATH)
    )
    return response

@router.get(
    '/groups/{id}',
    response_model=AppResponse[models.ProjectGroupOut],
    status_code=status.HTTP_200_OK,
    description='Get a specific project group by ID.'
)
@rate_limiter(80, 'minute')
async def get_project_group(
        request: Request,
        id: str = Path(
            ...,
            description='ID of the project group to retrieve.'
        ),
        lang: Language = Query(
            DEFAULT_LANGUAGE,
            description='Language for the project data.'
        )
    ) -> AppResponse[models.ProjectGroupOut]:
    '''
    GET /projects/groups/{id}\n
    Content-type: application/json\n
    <br>
    Get a specific project group by ID.
    '''
    __curr_path__: str = f'{PATH}/groups/{id}'
    
    payload: models.ProjectGroupOut = services.fetch_project_group(id, lang, path=__curr_path__)
    response: AppResponse[models.ProjectGroupOut] = AppResponse(
        success=True,
        error=None,
        message='Project group was successfully obtained.',
        data=payload,
        meta=AppResponse.MetaData(path=__curr_path__)
    )
    return response



@router.post(
    '/',
    response_model=AppResponse[models.PostContentResponse],
    status_code=status.HTTP_201_CREATED,
    description='Create a new project.'
)
@security.required_permissions(security.PERMITS.MAINTAINER)
@rate_limiter(60, 'minute')
async def create_project(
        request: Request,
        body: models.ProjectIn
    ) -> AppResponse[models.PostContentResponse]:
    '''
    POST /projects\n
    Content-type: application/json\n
    <br>
    Create a new project.
    '''
    
    response: models.PostContentResponse = services.create_project(body, path=PATH)
    return AppResponse(
        success=True,
        error=None,
        message='New Project successfully created.',
        data=response,
        meta=AppResponse.MetaData(path=PATH)
    )



@router.put(
    '/{id}',
    response_model=AppResponse[models.PostContentResponse],
    status_code=status.HTTP_200_OK,
    description='Edit an existing project by ID.'
)
@security.required_permissions(security.PERMITS.MAINTAINER)
@rate_limiter(30, 'minute')
async def edit_project(
        request: Request,
        body: models.ProjectIn,
        id: str = Path(
            ...,
            description=''
        )
    ) -> AppResponse[models.PostContentResponse]:
    '''
    PUT /projects/{id}\n
    Content-type: application/json\n
    <br>
    Edit an existing project by ID.
    '''
    
    __curr_path__: str = f'{PATH}/{id}'
    response_message: str
    response_data: models.PostContentResponse
    
    if not services.exist_project(id, path=__curr_path__):
        response_data = services.create_project(body, path=__curr_path__)
        response_message = 'New Project successfully created.'
    else:
        response_data = services.replace_project(id, body, path=__curr_path__)
        response_message = 'Project was successfully edited.'
    
    return AppResponse(
        success=True,
        error=None,
        message=response_message,
        data=response_data,
        meta=AppResponse.MetaData(path=__curr_path__)
    )



@router.delete(
    '/',
    response_model=AppResponse,
    status_code=status.HTTP_200_OK,
    description='Delete all projects.'
)
@security.required_permissions(security.PERMITS.OWNER)
@rate_limiter(10, 'minute')
async def delete_all_projects(
        request: Request,
        confirm: bool = Query(
            False,
            description='Confirmation to delete all Projects.'
        )
    ) -> AppResponse:
    '''
    DELETE /projects\n
    Content-type: application/json\n
    <br>
    Delete all projects.
    '''
    
    services.delete_projects(confirm)
    return AppResponse(
        success=True,
        error=None,
        message=f'All my Projects were successfully deleted.',
        data=None,
        meta=AppResponse.MetaData(path=PATH)
    )

@router.delete(
    '/{id}', 
    response_model=AppResponse,
    status_code=status.HTTP_200_OK,
    description='Delete a specific project by ID.'
)
@security.required_permissions(security.PERMITS.MAINTAINER)
@rate_limiter(10, 'minute')
async def delete_project(
        request: Request,
        id: str = Path(
            ...,
            description='ID of the project to delete.'
        )
    ) -> AppResponse:
    '''
    DELETE /projects/{id}\n
    Content-type: application/json\n
    <br>
    Delete a specific project by ID.
    '''

    len_before: int = services.sizeof_db()
    services.delete_project(id, path=PATH)
    len_after: int = services.sizeof_db()
    
    return AppResponse(
        success=True,
        error=None,
        message=f'{len_before - len_after} of my Projects were successfully deleted.',
        data={
            'id': id
        },
        meta=AppResponse.MetaData(path=f'{PATH}/{id}')
    )
