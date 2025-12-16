
from typing import Optional, Any
from unicodedata import name
from pymongo import ReturnDocument

from app.core.db import projects_collection as PROJECTS
from app.core.consts import DEFAULT_LANGUAGE
from app.core.types import Language
from app.utils.i18n import translate
from app.data.projects.models import *
from app.data.projects.types import project_t, project_group_t
from app.data.projects.errors import InvalidProjectId, InvalidProjectObject, InvalidProjectType, ConfirmRequiredAction

sizeof_db = lambda : PROJECTS.count_documents({})

# ╔══════════════════════════════╗ #
# ║       SERVICE FEATURES       ║ #
# ╚══════════════════════════════╝ #
def __next_id__() -> int:
    counter = PROJECTS.database.counters.find_one_and_update(
        { '_id': 'projects' },
        { '$inc': { 'value': 1 } },
        upsert=True,
        return_document=ReturnDocument.AFTER
    )
    return counter['value']

def __format_id__(id: int | str, *, path: Optional[str] = None) -> int:
    try:
        return int(id)
    except:
        raise InvalidProjectId(id, path).throw()

def __dumper__(
        project: project_t,
        lang: Language = DEFAULT_LANGUAGE,
        *, 
        path: Optional[str] = None
    ) -> ProjectOut:
    
    payload: dict[str, Any]
    try:
        payload = project.copy()
    except:
        raise InvalidProjectObject(project, path).throw()

    payload.pop('_id', None)
    payload.setdefault('id', None)

    # description
    translate(payload, lang,
        'description',
        path=path
    )

    # default
    payload.setdefault('tech_stack', [])
    payload.setdefault('links', {})

    return ProjectOut(**payload)



# ╔══════════════════════════════╗ #
# ║   PROJECT SERVICE FEATURES   ║ #
# ╚══════════════════════════════╝ #
def exist_project(id: int, *, path: Optional[str] = None) -> bool:
    id: int = __format_id__(id, path=path)
    result: Any | None = PROJECTS.find_one({ 'id': id })
    
    return result is not None

def fetch_project(id: int, lang: Language = DEFAULT_LANGUAGE, *, path: Optional[str] = None) -> ProjectOut:
    id: int = __format_id__(id, path=path)
    
    payload: dict[str, Any] | None = PROJECTS.find_one({ 'id': id })
    return __dumper__(payload, lang, path=path)

def load_projects(lang: Language = DEFAULT_LANGUAGE, *, path: Optional[str] = None) -> list[ProjectOut]:
    cursor = PROJECTS.find({}).sort('id', 1)
    
    return [
        __dumper__(doc, lang, path=path)
        for doc in cursor
    ]

def fetch_project_groups(lang: Language = DEFAULT_LANGUAGE, *, path: Optional[str] = None) -> list[ProjectGroupOut]:
    cursor = PROJECTS.find({}).sort('id', 1)
    
    payload: dict[str, project_group_t] = {}
    for doc in cursor:
        type_project: str = doc.get('type', 'Project')
        if type_project not in payload:
            payload[type_project] = {
                'type': type_project,
                'projects': []
            }
        
        payload[type_project]['projects'].append(__dumper__(doc, lang, path=path).dict())
    
    payload=[
        ProjectGroupOut(**group)
        for group in payload.values()
    ]
    return payload

def fetch_project_group(id: str, lang: Language = DEFAULT_LANGUAGE, *, path: Optional[str] = None) -> ProjectGroupOut:
    cursor = PROJECTS.find({ 'type': id }).sort('id', 1)
    
    if cursor.count() == 0:
        raise InvalidProjectType(id, path).throw()
    
    payload: project_group_t = {
        'type': id,
        'projects': []
    }
    for doc in cursor:
        payload['projects'].append(__dumper__(doc, lang, path=path).dict())
    
    return ProjectGroupOut(**payload)

def add_project(obj: Project) -> PostContentResponse:
    project_id: int = __next_id__()
    
    payload: dict[str, Any] = { 'id': project_id } | obj.dump()
    result = PROJECTS.insert_one(payload)

    return PostContentResponse(
        id=payload['id'],
        name=obj.name,
        type=obj.type
    )

def create_project(request: ProjectIn, *, path: Optional[str] = None) -> PostContentResponse:
    ''' Create a new project and adding automatically to DB '''
    # check errors
    if not request:
        raise InvalidProjectObject(None, path).throw()
    
    # builders
    PROJECT_BUILDERS: dict[str, Project] = {
        'WebProject': WebProject,
        'Project': Project,
    }

    # get payload and the type of project
    payload: dict[str, Any] = request.model_dump()
    type_project: str = payload.pop('type', 'Project')

    project_cls: Project = PROJECT_BUILDERS.get(type_project)

    if project_cls is None:
        raise InvalidProjectType(type_project, path, status_code=500).throw()

    # if builder is <Project> then we have type kwarg to pass
    obj: Project
    if project_cls is Project:
        obj = project_cls(type=type_project, **payload)
    else:
        obj = project_cls(**payload)

    return add_project(obj)

def replace_project(id: int, request: ProjectIn, *, path: Optional[str] = None) -> PostContentResponse:
    id: int = __format_id__(id, path=path)

    if not request:
        raise InvalidProjectObject(None, path).throw()

    payload: dict[str, Any] = request.model_dump()
    type_project: str = payload.pop('type', 'Project')

    PROJECT_BUILDERS: dict[str, Project] = {
        'WebProject': WebProject,
        'Project': Project,
    }

    project_cls: Project = PROJECT_BUILDERS.get(type_project)
    if project_cls is None:
        raise InvalidProjectType(type_project, path, status_code=500).throw()

    obj: Project
    if project_cls is Project:
        obj = project_cls(type=type_project, **payload)
    else:
        obj = project_cls(**payload)

    doc: dict[str, Any] = { 'id': id } | obj.dump()

    result: Any = PROJECTS.find_one_and_replace({ 'id': id }, doc, return_document=ReturnDocument.AFTER)
    if result is None:
        raise InvalidProjectId(id, path).throw()

    return PostContentResponse(
        id=id,
        name=obj.name,
        type=obj.type
    )

def delete_project(id: int, *, path: Optional[str] = None) -> None:
    id: int = __format_id__(id, path=path)
    
    result = PROJECTS.delete_one({ 'id': id })
    if result.deleted_count == 0:
        raise InvalidProjectId(id, path).throw()

def delete_projects(confirm: bool = False, *, path: Optional[str] = None) -> None:
    if not confirm:
        raise ConfirmRequiredAction(path).throw()
    
    PROJECTS.delete_many({})
