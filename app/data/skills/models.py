
from typing import Optional
from pydantic import BaseModel, Field

from app.core.types import Translations

# ╔══════════════════════════════╗ #
# ║        CONTENT MODELS        ║ #
# ╚══════════════════════════════╝ #
class SkillIn(BaseModel):
    name: str                      = Field(..., description='Name of the skill')
    experience: int                = Field(..., description='Years of experience with the skill')
    description: Translations[str] = Field(..., description='Description of the skill in multiple languages')
    icon_source: str               = Field(..., description='Source URL or path for the skill icon')
    code_example: str              = Field(..., description='Code example demonstrating the skill')

class SkillOut(BaseModel):
    name: str         = Field(..., description='Name of the skill')
    experience: int   = Field(..., description='Years of experience with the skill')
    description: str  = Field(..., description='Description of the skill in multiple languages')
    icon_source: str  = Field(..., description='Source URL or path for the skill icon')
    code_example: str = Field(..., description='Code example demonstrating the skill')

class SkillPatch(BaseModel):
    experience: Optional[int]                = Field(None, description='Years of experience with the skill')
    description: Optional[Translations[str]] = Field(None, description='Description of the skill in multiple languages')
    icon_source: Optional[str]               = Field(None, description='Source URL or path for the skill icon')
    code_example: Optional[str]              = Field(None, description='Code example demonstrating the skill')

