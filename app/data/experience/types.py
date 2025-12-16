
from typing import Any, TypedDict
from typing import Optional

from app.core.types import Translations

class companyinfo_t(TypedDict):
    name: str
    location: str
    zip_code: str
    industry: str
    website: Optional[str]
    fundation: str
    bankrupted: bool

class experience_t(TypedDict):
    _id: Optional[Any]
    role: str
    company: companyinfo_t
    start_date: str
    end_date: Optional[str]
    description: Translations[str]

