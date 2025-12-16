
from typing import TypedDict
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from pydantic import BaseModel

from app.core.consts import ROLES

# ╔══════════════════════════════╗ #
# ║        OAUTH2 SCHEME         ║ #
# ╚══════════════════════════════╝ #
oauth2 = OAuth2PasswordBearer(tokenUrl='/login')
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

# ╔══════════════════════════════╗ #
# ║       SECURITY STRUCTS       ║ #
# ╚══════════════════════════════╝ #
class token_t(TypedDict):
    sub: str
    role: str
    exp: int

class AuthToken(BaseModel):
    access_token: str
    token_type: str = 'bearer'
    role: ROLES = ROLES.USER
