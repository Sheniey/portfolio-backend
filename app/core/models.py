
from typing import Generic, Optional, Any
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime, timezone

from app.core.types import T

# ╔══════════════════════════════╗ #
# ║        GLOBAL MODELS         ║ #
# ╚══════════════════════════════╝ #
...

# ╔══════════════════════════════╗ #
# ║       GLOBAL RESPONSES       ║ #
# ╚══════════════════════════════╝ #
class AppResponse(BaseModel, Generic[T]):
    class MetaData(BaseModel):
        path: Optional[str] = Field(None, description='Request path or resource path (e.g. /api/users/me)')
        timestamp: str      = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
        version: str        = Field('v1', description='API version')
    
    success: bool           = Field(False, description='Indicates if the operation succeeded')
    error: Optional[str]    = Field(None, description='Error code or short name (UPPER_SNAKE_CASE)')
    message: Optional[str]  = Field(None, description='Human readable message')
    data: Optional[T]       = Field(None, description='Payload (any JSON-serializable structure)')
    meta: MetaData          = Field(default_factory=MetaData)

    model_config = ConfigDict(
        extra='forbid',
        frozen=False,
        validate_default=True
    )

    def __getitem__(self, key: Any) -> Any:
        if isinstance(self.data, dict):
            return self.data.get(key)
        raise TypeError(f'Cannot use indexing on data of type {type(self.data).__name__}')

    def get(self, key: Any, default: Any = None) -> Any:
        if isinstance(self.data, dict):
            return self.data.get(key, default)
        return default

