
from typing import Literal, TypedDict, Optional

from app.core.types import Translations

# ╔══════════════════════════════╗ #
# ║        CONTENT TYPES         ║ #
# ╚══════════════════════════════╝ #
class project_t(TypedDict):
    '''Estructura de un Projecto para los diccionarios.'''
    id: Optional[int]
    name: str
    type: str
    scale: Literal['learning', 'short', 'medium', 'long', 'enterprice', 'ecosystem']
    deployment: bool
    description: Translations[str]
    tech_stack: list[str]
    links: dict[str, str]

class project_group_t(TypedDict):
    '''Estructura de un Grupo de Proyectos para los diccionarios.'''
    id: Optional[int]
    name: str
    niche: str
    deployment: bool
    description: Translations[str]
    links: dict[str, str]
    subprojects: list[project_t]
