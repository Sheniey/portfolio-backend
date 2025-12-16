
from typing import Optional, Any

from app.core.db import experiences_collection as EXPERIENCES
from app.core.types import Language
from app.core.consts import DEFAULT_LANGUAGE
from app.utils.i18n import translate
from app.data.experience.models import ExperienceIn, ExperienceOut, PostContentResponse
from app.data.experience.types import experience_t
from app.data.experience.errors import InvalidExperienceObject, CompanyNameNotFound

def __dumper__(experience: experience_t, lang: Language = DEFAULT_LANGUAGE, *, path: Optional[str] = None) -> ExperienceOut:
    payload: Any

    print(experience.copy())

    try:
        payload = experience.copy()
        print(payload)
    except:
        raise InvalidExperienceObject(experience, path=path).throw()

    print('Hello')
    t = translate(payload, lang,
        'description',
        path=path
    )
    print(t)
    
    if payload.get('description') is not None:
        payload['description'] = ''
    
    return ExperienceOut(**payload)

def get_experience_list(lang: Language = DEFAULT_LANGUAGE, *, path: Optional[str] = None) -> list[ExperienceOut]:
    cursor = EXPERIENCES.find({})
    return [
        __dumper__(exp, lang, path=path)
        for exp in cursor
    ]
    
def get_experiences_by_company(company: str, lang: Language = DEFAULT_LANGUAGE, *, path: Optional[str] = None) -> list[ExperienceOut]:
    cursor = EXPERIENCES.find({'company': {'name': company}}, {'_id': 0})
    try:
        payload: list[ExperienceOut] = [
            __dumper__(exp, lang, path=path)
            for exp in cursor
        ]
    except InvalidExperienceObject:
        raise CompanyNameNotFound(company, path=path).throw()

    return payload

def make_new_experience(experience: ExperienceIn, *, path: Optional[str] = None) -> PostContentResponse:
    payload: experience_t

    try:
        payload = experience.model_dump()
    except:
        raise InvalidExperienceObject(experience, path=path).throw()
    
    EXPERIENCES.insert_one(payload)
    return PostContentResponse(
        role=experience.role,
        company=experience.company,
        description=experience.description
    )

def delete_experiences(*, path: Optional[str] = None) -> int:
    result = EXPERIENCES.delete_many({}, {'_id': 0})
    return result.deleted_count

def delete_experiences_by_company(company: str, *, path: Optional[str] = None) -> int:
    result = EXPERIENCES.delete_many({'company': {'name': company}}, {'_id': 0})
    return result.deleted_count