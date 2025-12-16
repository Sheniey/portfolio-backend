
from typing import Final as Const, Optional
from fastapi import APIRouter, status, Response, Query, Request
import json

from app.core.config import LOGGING_FILE
from app.core import models, errors
from app.utils import security
from app.utils.protection import rate_limiter

PATH: Const[str] = '/admin'
router: APIRouter = APIRouter(prefix=PATH, tags=['admin', 'owner'])

# ╔══════════════════════════════╗ #
# ║       ADMIN ENDPOINTS        ║ #
# ╚══════════════════════════════╝ #
@router.options(
    '/',
    response_class=Response,
    status_code=status.HTTP_204_NO_CONTENT,
    description='CORS preflight for /admin endpoint',
)
@rate_limiter(60, 'minute')
async def admin_options(request: Request) -> Response:
    '''
    OPTIONS /admin\n
    Content-Type: none\n
    <br>
    Return admin endpoint methods.
    '''
    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
        headers={
            'Allow': 'GET,OPTIONS'
        }
    )

@router.get(
    '/',
    response_model=models.AppResponse,
    status_code=status.HTTP_200_OK,
    description='Admin panel overview',
)
@security.required_permissions(security.PERMITS.OWNER)
@rate_limiter(10, 'minute')
async def admin_panel(request: Request) -> models.AppResponse:
    return models.AppResponse(
        success=True,
        error=None,
        message='Welcome to the admin panel',
        data={
            'available_endpoints': [
                '/admin',
                '/admin/logs'
            ]
        },
        meta=models.AppResponse.MetaData(
            path=PATH
        )
    )

@router.options(
    '/logs',
    response_class=Response,
    status_code=status.HTTP_204_NO_CONTENT,
    description='CORS preflight for /admin/logs endpoint',
)
@rate_limiter(60, 'minute')
async def logs_options(request: Request) -> Response:
    '''
    OPTIONS /admin/logs\n
    Content-Type: application/json\n
    <br>
    Return log endpoint options.
    '''
    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
        headers={
            'Allow': 'GET, DELETE, OPTIONS'
        }
    )

@router.get(
    '/logs',
    response_model=models.AppResponse,
    status_code=status.HTTP_200_OK,
    description='Download audit log file',
)
@security.required_permissions(security.PERMITS.OWNER)
@rate_limiter(15, 'minute')
async def get_logs(
        request: Request,
        last: Optional[str] = Query(
            None,
            description='Retrieve logs since this timestamp (ISO 8601 format)'
        )
    ) -> models.AppResponse:
    '''
    GET /admin/logs\n
    Content-Type: application/json\n
    <br>
    Retrieve audit log file contents.
    '''
    __curr_path__ = f'{PATH}/logs'
    
    if last is None:
        last = '0'
    
    with open(LOGGING_FILE, 'r') as f:
        try:
            logs: dict[str, str | int] = json.load(f)
        except (json.JSONDecodeError|FileNotFoundError):
            raise errors.AppException(
                model=models.AppResponse(
                    success=False,
                    error='LOGS_NOT_FOUND',
                    message='Failed to retrieve audit logs',
                    data=None,
                    meta=models.AppResponse.MetaData(
                        path=__curr_path__
                    )
                ),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    try:
        logs_items: list[dict[str, str | int]] = list(logs.items())
        if int(last):
            logs_items = logs_items[-int(last):]
        logs_return: dict[str, str | int] = {k: v for k, v in logs_items}
    except:
        raise errors.AppException(
            model=models.AppResponse(
                success=False,
                error='INVALID_LAST_QUERY',
                message='The "last" query parameter is invalid',
                data={
                    'provided_value': last
                },
                meta=models.AppResponse.MetaData(
                    path=__curr_path__
                )
            ),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    return models.AppResponse(
        success=True,
        error=None,
        message='Audit logs retrieved successfully',
        data=logs_return,
        meta=models.AppResponse.MetaData(
            path=__curr_path__
        )
    )

@router.delete(
    '/logs',
    response_model=models.AppResponse,
    status_code=status.HTTP_200_OK,
    description='Delete audit log file contents',
)
@security.required_permissions(security.PERMITS.OWNER)
@rate_limiter(5, 'minute')
async def clear_logs(request: Request) -> models.AppResponse:
    '''
    DELETE /admin/logs\n
    Content-Type: application/json\n
    <br>
    Clear audit log file contents.
    '''
    __curr_path__ = f'{PATH}/logs'
    
    with open(LOGGING_FILE, 'w+') as f:
        length: int = len(json.load(f))
        json.dump({}, f)

    return models.AppResponse(
        success=True,
        error=None,
        message='Audit logs cleared successfully',
        data={
            'deleted_entries': length
        },
        meta=models.AppResponse.MetaData(
            path=__curr_path__
        )
    )
