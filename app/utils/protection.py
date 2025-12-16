
from typing import Any, Literal
from functools import wraps

from app.core.config import RATE_LIMIT_REQUESTS, RATE_LIMIT_PERIOD
from app.core.types import F, P, R
from app.core.protection import limiter

__all__ = [
    'rate_limiter'
]

# ╔══════════════════════════════╗ #
# ║      RATE LIMITER HOOK       ║ #
# ╚══════════════════════════════╝ #
def rate_limiter(
        queries: int = RATE_LIMIT_REQUESTS,
        per: Literal['second', 'minute', 'hour', 'day'] = RATE_LIMIT_PERIOD
    ) -> F[P, R]:
    '''
    Limitador de tasa de consultas para evitar DDoS con las rutas de la API.
    
    :param queries: Número máximo de consultas permitidas por el periodo definido.
    :type queries: int
    :param per: Periodo por el cual limitar las consultas.
    :type per: Literal['second', 'minute', 'hour', 'day']
    
    :return: Endpoint decorado con limitador de tasa.
    :rtype: F[P, R]
    '''
    def decorator(func: F[P, R]) -> F[P, R]:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> R:
            return await func(*args, **kwargs)
        
        return limiter.limit(f'{queries}/{per}')(wrapper)
    
    return decorator
