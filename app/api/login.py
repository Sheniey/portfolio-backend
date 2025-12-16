
from typing import Final as Const
from fastapi import APIRouter, Depends, Request, status
from fastapi.security import OAuth2PasswordRequestForm

from app.core.config import OWNER_PASSWORD_HASH, MAINTAINER_PASSWORD_HASH
from app.core.security import AuthToken, ROLES
from app.utils import security
from app.utils.protection import rate_limiter

PATH: Const[str] = '/login'
router: APIRouter = APIRouter(prefix=PATH, tags=['auth'])

# ╔══════════════════════════════╗ #
# ║        LOGIN ENDPOINT        ║ #
# ╚══════════════════════════════╝ #
@router.post(
    '/',
    response_model=AuthToken,
    status_code=status.HTTP_202_ACCEPTED
)
@rate_limiter(10, 'minute')
def login(request: Request, form: OAuth2PasswordRequestForm = Depends()) -> AuthToken:
    '''
    POST /login\n
    Content-Type: application/x-www-form-urlencoded\n
    <br>
    Authenticate user and return an access token.
    '''
    subject: str = form.username
    password: str = form.password
    
    role: ROLES = ROLES.USER
    for password_hash, permit in {
        OWNER_PASSWORD_HASH: ROLES.OWNER,
        MAINTAINER_PASSWORD_HASH: ROLES.MAINTAINER
    }.items():
        if security.verify_password(password, password_hash):
            role = permit
            break

    token: str = security.create_token({ 'sub': subject, 'role': role.value })

    return AuthToken(
        access_token  = token,
        token_type    = 'bearer',
        role          = role.value
    )
