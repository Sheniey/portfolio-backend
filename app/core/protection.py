
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.core.config import RATE_LIMIT_REQUESTS, RATE_LIMIT_PERIOD

__all__ = ['limiter']

# ╔══════════════════════════════╗ #
# ║       DDOS PROTECTION        ║ #
# ╚══════════════════════════════╝ #
limiter: Limiter = Limiter(key_func=get_remote_address, default_limits=[f'{RATE_LIMIT_REQUESTS}/{RATE_LIMIT_PERIOD}'])
