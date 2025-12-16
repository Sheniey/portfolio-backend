
from typing import Optional, Any
from pydantic import BaseModel, Field

from app.core.types import Translations
from app.data.experience.types import companyinfo_t

class CompanyInfo(BaseModel):
    name: str               = Field(..., description='Name of the company')
    location: str           = Field(..., description='Location of the company')
    zip_code: str           = Field(..., description='ZIP code of the company')
    industry: str           = Field(..., description='Industry sector of the company')
    website: Optional[str]  = Field(None, description='Website URL of the company')
    fundation: str          = Field(..., description='Foundation year of the company')
    bankrupted: bool        = Field(False, description='Indicates if the company is bankrupted')

class ExperienceIn(BaseModel):
    role: str                       = Field(..., description='Job title or role held')
    company: CompanyInfo            = Field(..., description='Information about the company')
    start_date: str                 = Field(..., description='Start date of the experience')
    end_date: Optional[str]         = Field(None, description='End date of the experience')
    description: Translations[str]  = Field(..., description='Description of the experience')

class ExperienceOut(BaseModel):
    _id: Optional[Any]
    role: str               = Field(..., description='Job title or role held')
    company: CompanyInfo    = Field(..., description='Information about the company')
    start_date: str         = Field(..., description='Start date of the experience')
    end_date: Optional[str] = Field(None, description='End date of the experience')
    description: str        = Field(..., description='Description of the experience')
    
    class Config:
        extra = 'allow'

class PostContentResponse(BaseModel):
    role: str                       = Field(..., description='Job title or role held')
    company: CompanyInfo            = Field(..., description='Information about the company')
    description: Translations[str]  = Field(..., description='Description of the experience')
