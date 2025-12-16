
from typing import Literal, Optional
from pydantic import BaseModel, Field

from app.core.consts import DEFAULT_LANGUAGE
from app.core.types import Language, Translations
from app.utils.i18n import use_translation
from app.data.projects.consts import DEFAULT_LINKS
from app.data.projects.types import project_group_t, project_t

# ╔══════════════════════════════╗ #
# ║        CONTENT MODELS        ║ #
# ╚══════════════════════════════╝ #
class ProjectIn(BaseModel):
    # POST|PUT|PATCH Method
    #   User -> Server
    name: str
    type: str
    scale: Literal['learning', 'short', 'medium', 'long', 'enterprice', 'ecosystem'] = 'short'
    deployment: bool = False
    description: Translations[str] = Field(
        title='Project Description',
        description='the description of the project must be same this: { "lang-short": "description in that language", "en": "test description" }',
        default_factory=lambda : { 'en': 'None, english description', 'es': 'None, descripción en español' }
    )
    tech_stack: list[str] = Field(
        title='Teck Stack',
        description='list with techs used on the project.',
        default_factory=list
    )
    links: dict[str, str] = Field(
        title='Links',
        description='any links of the project, e.g., "git", "site", "blog"... and this must be a dictionary same like this: { "git": "/url/" }',
        default_factory=lambda : DEFAULT_LINKS
    )

class ProjectOut(BaseModel):
    # GET Method
    #   Server -> User
    id: Optional[int] = None
    name: str
    type: str
    scale: Literal['learning', 'short', 'medium', 'long', 'enterprice', 'ecosystem'] = 'short'
    deployment: bool = False
    description: str = Field(default_factory=lambda : 'None, could not load description')
    tech_stack: list[str] = Field(default_factory=list)
    links: dict[str, str] = Field(default_factory=lambda : DEFAULT_LINKS)
    
    class Config:
        extra = 'allow'

class ProjectGroupIn(BaseModel):
    # POST|PUT|PATCH Method
    #   User -> Server
    name: str
    niche: str
    deployment: bool = False
    description: Translations[str] = Field(
        title='Project Group Description',
        description='the description of the project group must be same this: { "lang-short": "description in that language", "en": "test description" }',
        default_factory=lambda : { 'en': 'None, english description', 'es': 'None, descripción en español' }
    )
    links: dict[str, str] = Field(
        title='Links',
        description='any links of the project group, e.g., "git", "site", "blog"... and this must be a dictionary same like this: { "git": "/url/" }',
        default_factory=lambda : DEFAULT_LINKS
    )
    subprojects: list[project_t] = Field(
        title='Subprojects',
        description='list of subprojects as [{id, name, type}, {id, name. type}] to reference to all projects in the project group.',
        default_factory=list['PostContentResponse']
    )

class ProjectGroupOut(BaseModel):
    # GET Method
    #   Server -> User
    id: Optional[int] = None
    name: str
    niche: str
    deployment: bool = False
    description: str = Field(default_factory=lambda : 'None, could not load description')
    links: dict[str, str] = Field(default_factory=lambda : DEFAULT_LINKS)
    subprojects: list[project_t] = Field(default_factory=list)

class PostContentResponse(BaseModel):
    # POST|PUT|PATCH Method
    #   Server -> User
    id: int
    name: str
    type: str

# ╔══════════════════════════════╗ #
# ║        PROJECT MODELS        ║ #
# ╚══════════════════════════════╝ #
class Project:
    def __init__(self,
            name: str,
            type: str,
            *,
            # learning (tictactoe: 1s) | short (bigibai: 2s) | medium (royale-api: 3s) | long (spotify: 4s) | enterprice (chatgpt: 5s) | ecosystem (google: >6s)
            scale: Literal['learning', 'short', 'medium', 'long', 'enterprice', 'ecosystem'] = 'short',
            deployment: bool = False,
            description: Translations[str] = None,
            tech_stack: list[str] = '',
            links: dict[str, str] = None
        ) -> None:
        
        self.__name: str = name
        self.__type: str = type
        self.__scale: Literal['learning', 'short', 'medium', 'long', 'enterprice', 'ecosystem'] = scale
        self.__deployment: bool = deployment
        self.__description: Translations[str] = description or { 'es': '', 'en': '' }
        self.__tech_stack: list[str] = tech_stack
        self.__links: dict[str, str] = links or DEFAULT_LINKS
    
    @property
    def name(self) -> str: return self.__name
    
    @property
    def type(self) -> str: return self.__type
    
    @property
    def scale(self) -> str: return self.__scale
    
    def is_deployment(self) -> bool: return self.__deployment
    
    @property
    def description(self) -> Translations[str]: return self.__description
    
    @property
    def tech_stack(self) -> list[str]: return self.__tech_stack
    
    @property
    def links(self) -> dict[str, str]: return self.__links
    
    def add_link(self, source: str, url: str) -> None:
        self.__links[source] = url
    
    def dump(self, lang: Optional[Language] = None) -> project_t:
        return {
            'name': self.__name,
            'type': self.__type,
            'scale': self.__scale,
            'deployment': self.__deployment,
            'description': use_translation(self.__description, lang),
            'tech_stack': self.__tech_stack,
            'links': self.__links
        }
    
    def must_has(self) -> tuple[str]:
        keys: tuple[str] = tuple(self.dump().keys())
        return keys

class ProjectGroup:
    def __init__(self,
            name: str,
            niche: str,
            *,
            scale: Literal['learning', 'short', 'medium', 'long', 'enterprice', 'ecosystem'] = 'enterprice',
            deployment: bool = False,
            description: Translations[str] = None,
            links: dict[str, str] = None,
            projects: list[Project] = None
        ) -> None:
        
        self.__name: str = name
        self.__niche: str = niche
        self.__scale: Literal['learning', 'short', 'medium', 'long', 'enterprice', 'ecosystem'] = scale
        self.__deployment: bool = deployment
        self.__description: Translations[str] = description or { 'es': '', 'en': '' }
        self.__links: dict[str, str] = links or DEFAULT_LINKS
        self.__projects: list[Project] = projects or []

    @property
    def name(self) -> str: return self.__name
    
    @property
    def niche(self) -> str: return self.__niche

    @property
    def scale(self) -> Literal['learning', 'short', 'medium', 'long', 'enterprice', 'ecosystem']: return self.__scale
    
    @property
    def subprojects(self) -> list[Project]: return self.__projects
    
    @property
    def deployment(self) -> bool: return self.__deployment

    @property
    def description(self) -> Translations[str]: return self.__description

    @property
    def links(self) -> dict[str, str]: return self.__links
    
    def add_project(self, project: Project) -> None:
        self.__projects.append(project)
    
    def add_link(self, source: str, url: str) -> None:
        self.__links[source] = url
    
    def dump(self, lang: Optional[Language] = None) -> project_group_t:
        return {
            'name': self.__name,
            'niche': self.__niche,
            'deployment': self.__deployment,
            'description': use_translation(self.__description, lang),
            'links': self.__links,
            'subprojects': [
                project.dump(lang) for project in self.__projects
            ]
        }

# ╔══════════════════════════════╗ #
# ║      SPECIFIC PROJECTS      ║ #
# ╚══════════════════════════════╝ #
class WebProject(Project):
    def __init__(self,
            name: str,
            *,
            scale: Literal['learning', 'short', 'medium', 'long', 'enterprice', 'ecosystem'] = 'short',
            deployment: bool = False,
            description: Translations[str] = None,
            stack_end: Literal['frontend', 'backend', 'fullstack'] = 'fullstack',
            tech_stack: list[Literal[
                'HTML',
                'CSS',
                'JavaScript',
                'TypeScript',
                'Astro.js',
                'React.js',
                'Next.js'
            ]] = None,
            links: dict[str, str] = None
        ) -> None:
        
        super().__init__(
            name,
            type='Web Project',
            scale=scale,
            deployment=deployment,
            description=description or { 'es': '', 'en': '' },
            tech_stack=tech_stack or [],
            links=links or { **DEFAULT_LINKS, 'site': 'https://sheney-portfolio.vercel.com' }
        )
        self.__stackend: Literal['frontend', 'backend', 'fullstack'] = stack_end
    
    @property
    def stack_end(self) -> Literal['frontend', 'backend', 'fullstack']: return self.__stackend
    
    def dump(self, lang: Optional[Language] = None) -> project_t:
        payload: project_t = super().dump(lang)
        payload.update({ 'stack_end': self.__stackend })
        return payload

class DevOpsProject(Project):
    def __init__(self,
            name: str,
            *,
            scale: Literal['learning', 'short', 'medium', 'long', 'enterprice', 'ecosystem'] = 'short',
            deployment: bool = False,
            description: Translations[str] = None,
            platform: Literal['AWS', 'Azure', 'GCP', 'DigitalOcean', 'Heroku', 'Vercel', 'Netlify'] = 'AWS',
            tech_stack: list[Literal[
                'Docker',
                'Kubernetes',
                'Terraform',
                'Ansible',
                'Jenkins'
            ]] = None,
            links: dict[str, str] = None
        ) -> None:
        
        super().__init__(
            name,
            type='DevOps Project',
            scale=scale,
            deployment=deployment,
            description=description or { 'es': '', 'en': '' }, 
            tech_stack=tech_stack or [],
            links=links or { **DEFAULT_LINKS, 'site': 'https://sheney-portfolio.vercel.com' }
        )
        self.__platform: Literal['AWS', 'Azure', 'GCP', 'DigitalOcean', 'Heroku', 'Vercel', 'Netlify'] = platform
    
    @property
    def platform(self) -> None: return self.__platform
    
    def dump(self, lang: Optional[Language] = None) -> project_t:
        payload: project_t = super().dump(lang)
        payload.update({ 'platform': self.__platform })
        return payload

class EcosystemProject(ProjectGroup):
    def __init__(self,
            name: str,
            niche: str = 'Diverse',
            *,
            description: Translations[str] = None,
            links: dict[str, str] = None,
            subprojects: list[Project] = None
        ) -> None:
        
        super().__init__(
            name,
            scale='ecosystem',
            niche=niche,
            deployment=True,
            description=description or { 'es': '', 'en': '' },
            links=links or DEFAULT_LINKS,
            projects=subprojects or []
        )
    
    
