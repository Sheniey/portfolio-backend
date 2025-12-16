
import dotenv, os, random

from app.core.security import pwd_context
from app.core.consts import JWT_ALGORITHMS

__all__ = [
    'MONGO_URL',
    'SECRET_KEY',
    'ALGORITHM',
    'ACCESS_TOKEN_EXPIRE',
    'LOGGING_FILE',
    'OWNER_PASSWORD_HASH',
    'MAINTAINER_PASSWORD_HASH',
    'RATE_LIMIT_REQUESTS',
    'RATE_LIMIT_PERIOD',
]

dotenv.load_dotenv(
    dotenv_path=dotenv.find_dotenv('.env', True)
)

# ╔══════════════════════════════╗ #
# ║         DB VARIABLES         ║ #
# ╚══════════════════════════════╝ #
MONGO_URL: str | None = os.getenv('MONGO_URL')

# ╔══════════════════════════════╗ #
# ║        .ENV VARIABLES        ║ #
# ╚══════════════════════════════╝ #
SECRET_KEY: str | None = os.getenv('SECRET_KEY', f's3Cr3T.K3y-s33D:#{random.randint(0, 999_999_999_999_999):015d}') # 32-chars secret signature 
ALGORITHM: str = os.getenv('ALGORITHM', JWT_ALGORITHMS.HS256) # encrypt/decrypt algorithm
ACCESS_TOKEN_EXPIRE: int = int(os.getenv('ACCESS_TOKEN_EXPIRE', 60))  # kill token in 1 hour

# ╔══════════════════════════════╗ #
# ║      LOGGING VARIABLES       ║ #
# ╚══════════════════════════════╝ #
LOGGING_FILE: str = os.getenv('AUDIT_LOG_FILE', 'logs/audit.log')

# ╔══════════════════════════════╗ #
# ║        ROLE PASSWORDS        ║ #
# ╚══════════════════════════════╝ #
__0wbuñi3R_P4st0uwurD: str = os.getenv('OWNER_PASSWORD', '')
__M4iñt4iñi3R_P4st0uwurD: str = os.getenv('MAINTAINER_PASSWORD', '')

OWNER_PASSWORD_HASH: str = (
    pwd_context.hash(__0wbuñi3R_P4st0uwurD) if __0wbuñi3R_P4st0uwurD else None
)
MAINTAINER_PASSWORD_HASH: str = (
    pwd_context.hash(__M4iñt4iñi3R_P4st0uwurD) if __M4iñt4iñi3R_P4st0uwurD else None
)

# ╔══════════════════════════════╗ #
# ║     PROTECTION VARIABLES     ║ #
# ╚══════════════════════════════╝ #
RATE_LIMIT_REQUESTS: int = int(os.getenv('RATE_LIMIT_REQUESTS', 60))
RATE_LIMIT_PERIOD: str = os.getenv('RATE_LIMIT_PERIOD', 'minute')
