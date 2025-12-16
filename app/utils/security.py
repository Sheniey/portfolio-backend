
from typing import Any, Callable
from fastapi import Depends, Request
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from functools import wraps
from enum import Enum
import inspect

from app.core.types import F, P, R
from app.core.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE
from app.core.security import ROLES, oauth2, pwd_context, token_t
from app.core.errors import Unauthorized
from app.middlewares.request_var import get_curr_request

__all__ = [
    'PERMITS',
    'hash_password', 'verify_password',
    'create_token', 'curr_role',
    'required_permissions'
]

# ╔══════════════════════════════╗ #
# ║        SECURITY UTILS        ║ #
# ╚══════════════════════════════╝ #
class PERMITS(Enum):
    OWNER       = (ROLES.OWNER,)
    MAINTAINER  = (ROLES.OWNER, ROLES.MAINTAINER,)
    USER        = (ROLES.OWNER, ROLES.MAINTAINER, ROLES.USER,)

def hash_password(pwd: str, /) -> None:
    return pwd_context.hash(pwd)

def verify_password(plain_pwd: str, hashed_pwd: str, /) -> bool:
    return pwd_context.verify(plain_pwd, hashed_pwd)

def create_token(payload: token_t) -> str:
    to_encode: dict[str, Any] = payload.copy()
    
    # expire = now() + (ACCESS_TOKEN_EXPIRE || 15m.)
    expire: int = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE or 15)
    
    to_encode.update({ 'exp': expire })
    token: str = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token

def curr_role(token: str = Depends(oauth2), /) -> ROLES:
    try:
        payload: dict[str, Any] = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        role: str = payload.get('role')
        
        if not role:
            raise Unauthorized('Invalid token', 'UNAUTHORIZED').throw()
        
        return role
    
    except JWTError:
        raise Unauthorized('Invalid token', 'UNAUTHORIZED').throw()

def required_permissions(*allowed: ROLES | PERMITS) -> Callable[[F], F]:
    """
    Decorador que analiza los permisos necesarios y los actuales para poder ejecutar un endpoint, o no...
    
    @param allowed : lista de roles permitidos o simplemente permisos
    """
    
    allowed_roles: list[ROLES] = []
    for _ in allowed:
        if isinstance(_, PERMITS):
            allowed_roles.extend(_.value)
        elif isinstance(_, ROLES):
            allowed_roles.append(_)
    
    def decorator(func: F) -> F:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> R:
            req: Request = get_curr_request()

            auth_header: str = req.headers.get('Authorization')
            if not auth_header or not auth_header.startswith('Bearer '):
                raise Unauthorized('Missing or invalid token header', 'UNAUTHENTICATED').throw()

            token: str = auth_header.split(' ')[1]
            permits: list[ROLES] = [r.value for r in allowed_roles]

            try:
                payload: token_t = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
                role: str = payload.get('role')
                
                if role not in permits:
                    raise Unauthorized('Not authorized', 'FORBIDDEN', role).throw()
                
            except JWTError:
                raise Unauthorized('Invalid token', 'UNAUTHORIZED').throw()

            if inspect.iscoroutinefunction(func):
                return await func(*args, **kwargs)
            else:
                return func(*args, **kwargs)

        return wrapper
    return decorator
