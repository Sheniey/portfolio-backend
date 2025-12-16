
from typing import Optional

from app.core.db import skills_collection as SKILLS
from app.core.consts import DEFAULT_LANGUAGE
from app.core.types import Language
from app.utils.i18n import translate
from app.data.skills.models import SkillIn, SkillOut, SkillPatch
from app.data.skills.types import skill_t
from app.data.skills.errors import InvalidSkillname

# ╔══════════════════════════════╗ #
# ║           FEATURES           ║ #
# ╚══════════════════════════════╝ #
def fetch_skill_info(skillname: str, lang: Language = DEFAULT_LANGUAGE, *, path: Optional[str] = None) -> SkillOut:
    payload: skill_t | None = SKILLS.find_one({'name': skillname}, {'_id': 0})
    
    if payload is None:
        raise InvalidSkillname(skillname, path=path).throw()

    translate(payload, lang,
        'description',
        path=path
    )
    return SkillOut(**payload)

def fetch_all_skills(lang: Language = DEFAULT_LANGUAGE) -> list[SkillOut]:
    payload: list[SkillOut] = []
    cursor: skill_t | None = SKILLS.find({}, {'_id': 0})
    
    for skill in cursor:
        translate(skill, lang,
            'description',
            path=None
        )
        payload.append(SkillOut(**skill))
    
    return payload

def update_skill(skillname: str, request: SkillIn, *, path: Optional[str] = None) -> None:
    skill: skill_t | None = SKILLS.find_one_and_replace(
        {'name': skillname},
        request.model_dump(),
        return_document=True
    )
    
    if skill is None:
        raise InvalidSkillname(skillname, path=path).throw()

def patch_skill(skillname: str, request: SkillPatch, *, path: Optional[str] = None) -> None:
    update_data: skill_t = {k: v for k, v in request.model_dump().items() if v is not None}
    
    skill: skill_t | None = SKILLS.find_one_and_update(
        {'name': skillname},
        {'$set': update_data},
        return_document=True
    )
    
    if skill is None:
        raise InvalidSkillname(skillname, path=path).throw()

def delete_skill(skillname: str, *, path: Optional[str] = None) -> None:
    result = SKILLS.delete_one({'name': skillname})
    
    if result.deleted_count == 0:
        raise InvalidSkillname(skillname, path=path).throw()
