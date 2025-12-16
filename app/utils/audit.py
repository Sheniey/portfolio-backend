
from typing import Any
import logging, json
from logging import LogRecord, Logger
from logging.handlers import RotatingFileHandler
from datetime import datetime, timezone

from app.core.config import LOGGING_FILE

__all__ = [
    'audit_logger'
]

# ╔══════════════════════════════╗ #
# ║            LOGGER            ║ #
# ╚══════════════════════════════╝ #
class JSONFormatter(logging.Formatter):
    def format(self, record: LogRecord) -> str:
        log: dict[str, Any] = {
            'ts': datetime.now(timezone.utc).isoformat(),
            'lvl': record.levelname,
            'msg': record.getMessage(),
        }

        if hasattr(record, 'extra_data'):
            log.update(record.extra_data)

        return json.dumps(log, ensure_ascii=False)

audit_logger: Logger = logging.getLogger('audit')
audit_logger.setLevel(logging.INFO)

handler: RotatingFileHandler = RotatingFileHandler(LOGGING_FILE, maxBytes=5_000_000, backupCount=10)
handler.setFormatter(JSONFormatter())

audit_logger.addHandler(handler)
audit_logger.propagate = False

