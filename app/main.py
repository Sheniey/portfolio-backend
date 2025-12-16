
from typing import Final as Const
from fastapi import FastAPI, Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse

from app.api import admin, login, myinfo, experience, skills, projects
from app.core import models, consts
from app.utils import security
from app.utils.protection import rate_limiter
from app.middlewares.request_var import RequestContextMiddleware
from app.middlewares.auth import AuditMiddleware

PATH: Const[str] = '/'
ROUTERS: Const[tuple] = (admin, login, myinfo, experience, skills, projects)
app: FastAPI = FastAPI()

# ╔══════════════════════════════╗ #
# ║      EXCEPTION HANDLER       ║ #
# ╚══════════════════════════════╝ #
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """
    Custom handler to unwrap FastAPI's default {"detail": ...} behavior
    and standardize API error responses.
    """
    
    if isinstance(exc.detail, dict):
        return JSONResponse(
            status_code=exc.status_code,
            content=exc.detail
        )
    
    return JSONResponse(
        content=models.AppResponse(
            success=False,
            error=exc.__class__.__name__.upper(),
            message=str(exc.detail),
            data=None,
            meta=models.AppResponse.MetaData(
                path=str(request.url).replace(str(request.base_url), '/')
            ),
        ).model_dump(),
        status_code=exc.status_code
    )

# ╔══════════════════════════════╗ #
# ║          MIDDLEWARE          ║ #
# ╚══════════════════════════════╝ #
app.add_middleware(RequestContextMiddleware)
app.add_middleware(AuditMiddleware)

# ╔══════════════════════════════╗ #
# ║           ROUTING            ║ #
# ╚══════════════════════════════╝ #
for router in ROUTERS:
    app.include_router(router.router)

# ╔══════════════════════════════╗ #
# ║        ROOT ENDPOINTS        ║ #
# ╚══════════════════════════════╝ #
@app.get(
    '/',
    response_model=models.AppResponse,
    status_code=status.HTTP_200_OK,
    description='Root endpoint to verify API is running.'
)
@rate_limiter(30, 'minute')
async def root(request: Request) -> models.AppResponse:
    '''
    GET /\n
    Content-Type: application/json\n
    <br>
    Root endpoint to verify API is running.
    '''
    return models.AppResponse(
        success=True,
        error=None,
        message='API is running successfully.',
        data={
            'available_endpoints': [router.PATH for router in ROUTERS],
            'note': 'Use GET method on the listed endpoints to test.'
        },
        meta=models.AppResponse.MetaData(path=PATH)
    )


@app.get(
    '/users/me',
    response_model=models.AppResponse,
    status_code=status.HTTP_200_OK,
    description='Get current user role.'
)
@rate_limiter(60, 'minute')
async def curr_role(request: Request, role: str = Depends(security.curr_role)) -> models.AppResponse:
    '''
    GET /users/me\n
    Content-Type: application/json\n
    <br>
    Get current user role.
    '''
    __curr_path__: Const[str] = '/users/me'
    
    return models.AppResponse(
        success=True,
        error=None,
        message='Current user role fetched successfully.',
        data={
            'role': role,
            'available_roles': [r.value for r in consts.ROLES]
        },
        meta=models.AppResponse.MetaData(path=__curr_path__)
    )
