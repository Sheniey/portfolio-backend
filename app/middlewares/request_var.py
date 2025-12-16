
from typing import Any, Awaitable, Callable
from starlette.requests import Request
from starlette.types import Scope, Receive, Send
from fastapi import Request
from contextvars import ContextVar, Token as ContextToken

__all__ = [
    "RequestContextMiddleware",
]

_request_var: ContextVar[Request] = ContextVar('request')

# ╔══════════════════════════════╗ #
# ║     REQUEST CONTEXT_VAR      ║ #
# ╚══════════════════════════════╝ #

class RequestContextMiddleware:
    """ Middleware que guarda el Request actual en un ContextVar """
    def __init__(self, app: Callable[[Scope, Receive, Send], Awaitable[Any]]) -> None:
        self.app: Callable[[Scope, Receive, Send], Awaitable[Any]] = app
    
    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope['type'] == 'http':
            request: Request = Request(scope, receive=receive)
            token: ContextToken[Request] = _request_var.set(request)
            
            try:
                await self.app(scope, receive, send)
                
            finally:
                _request_var.reset(token)
            
        else:
            await self.app(scope, receive, send)
    
def get_curr_request() -> Request:
    """ Devuelve la Request actual desde el ContextVar. """
    return _request_var.get()
