
from typing import TypedDict

from app.core.types import Translations

# ╔══════════════════════════════╗ #
# ║        CONTENT TYPES         ║ #
# ╚══════════════════════════════╝ #
class skill_t(TypedDict):
    name: str
    experience: int
    description: Translations[str]
    icon_source: str
    code_example: str

