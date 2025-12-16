
from typing import TypedDict

from app.core.types import Email

# ╔══════════════════════════════╗ #
# ║        CONTENT TYPES         ║ #
# ╚══════════════════════════════╝ #
class myinfo_t(TypedDict):
    full_name: str
    first_name: str
    last_name: str
    pseudonym: str
    pseudonym_ascii: str
    about_me: str
    phone: str
    email: str
    emails: list[Email]
    location: str
    born_date: str
