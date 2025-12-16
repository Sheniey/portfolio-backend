
from typing import Final as Const

from app.core.consts import http_verbs

METHODS_AVAILABLE: Const[dict[str, str]] = ', '.join(
    [
        http_verbs.GET,
        http_verbs.PUT,
        http_verbs.DELETE,
        http_verbs.OPTIONS,
        http_verbs.HEAD
    ]
)

DEFAULT_EMAIL: Const[str] = 'sheneyby2010@gmail.com'
DEFAULT_BIRTH: Const[str] = '2010-09-08'
DEFAULT_LOCATION: Const[str] = 'Unknown, Unknown, México'
