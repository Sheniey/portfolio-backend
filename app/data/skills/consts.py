
from typing import Final as Const

from app.core.consts import http_verbs

METHODS_AVAILABLE: Const[dict[str, str]] = ', '.join(
    [
        http_verbs.GET,
        http_verbs.PUT,
        http_verbs.PATCH,
        http_verbs.OPTIONS,
        http_verbs.HEAD
    ]
)
