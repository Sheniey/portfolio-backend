
from typing import Any, Awaitable, Callable
from starlette.requests import Request
from starlette.types import Scope, Receive, Send
from fastapi import Request
from urllib.parse import urlparse
from jose import jwt, JWTError
from datetime import datetime, timezone

from app.core.config import SECRET_KEY, ALGORITHM
from app.utils.audit import audit_logger

__all__ = [
    'AuditMiddleware'
]

# ╔══════════════════════════════╗ #
# ║         AUDIT LOGGER         ║ #
# ╚══════════════════════════════╝ #
class AuditMiddleware:
    """ Middleware global que registra cada request y su origen """
    def __init__(self, app: Callable[[Scope, Receive, Send], Awaitable[Any]]) -> None:
        self.app: Callable[[Scope, Receive, Send], Awaitable[Any]] = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope['type'] != 'http':
            return await self.app(scope, receive, send)
        
        req: Request = Request(scope, receive)
        start: datetime = datetime.now(timezone.utc)
        SUBJECT, ROLE, STATUS_CODE = None, None, None
        location_header, skip_log = None, False

        auth_header = req.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token: str = auth_header.split(' ', 1)[1].strip()
            try:
                payload: dict[str, Any] = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
                SUBJECT = payload.get('sub')
                ROLE = payload.get('role', 'user')
            except JWTError:
                ROLE = 'user'

        async def send_wrapper(message: dict[str, Any]) -> None:
            nonlocal STATUS_CODE, location_header
            if message['type'] == 'http.response.start':
                STATUS_CODE = message.get('status')
                raw_headers: list[tuple[bytes, bytes]] = message.get('headers', [])
                
                headers_dict = {name.lower(): value for name, value in raw_headers}
                location_header = headers_dict.get(b'location')
                if location_header:
                    location_header = location_header.decode('latin-1')
            await send(message)
        
        await self.app(scope, receive, send_wrapper)

        PATH: str = req.url.path
        METHOD: str = req.method
        IPV4: str = req.client.host if req.client else None
        USER_AGENT: str = req.headers.get('user-agent', '')
        DURATION_MS: float = (datetime.now(timezone.utc) - start).total_seconds() * 1000
        
        skip_log: bool
        if STATUS_CODE == 307 and location_header:
            try:
                loc_path = urlparse(location_header).path or ''
                if loc_path.rstrip('/') == PATH.rstrip('/'):
                    skip_log = False
            except Exception: skip_log = True

        if not skip_log:
            audit_logger.info('request_log', extra={'extra_data': {
                'sub': SUBJECT,
                'role': ROLE,
                'path': PATH,
                'method': METHOD,
                'status_code': STATUS_CODE,
                'ip': IPV4,
                'user_agent': USER_AGENT,
                'duration_ms': round(DURATION_MS, 2),
            }})
