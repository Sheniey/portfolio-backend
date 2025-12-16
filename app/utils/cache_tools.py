
from functools import lru_cache, wraps

from app.core.types import T, F, P, R

__all__ = [
    'cached'
]

# ╔══════════════════════════════╗ #
# ║         CACHE TOOLS          ║ #
# ╚══════════════════════════════╝ #
def cached(size: int, *, diff_types: bool = False) -> F[P, R]:
    '''
    Wrapper caché para `functools.lru_cache()` con sintaxis más amigable y consistente para los parametros.
    
    :param size: Tamaño máximo de la Caché.
    :type size: int
    :param diff_types: Diferenciar tipos en la Caché.
    :type diff_types: bool
    
    :return: Función Decorada.
    :rtype: F[P, R]
    '''
    def decorator(func: F[P, R]) -> F[P, R]:
        cached_func = lru_cache(
            maxsize=size,
            typed=diff_types
        )(func)
        @wraps(func)
        def wrapper(*args: T, **kwargs: T) -> R:
            return cached_func(*args, **kwargs)
        return wrapper
    return decorator
