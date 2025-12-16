
from typing import Final as Const, Literal, get_args
from dataclasses import dataclass
from enum import StrEnum

from app.core.types import Language

# ╔══════════════════════════════╗ #
# ║         SIMPLY CONST         ║ #
# ╚══════════════════════════════╝ #
SUPPORTED_LANGUAGES = get_args(Language)
DEFAULT_LANGUAGE: Const[Literal['en']] = 'en'

# ╔══════════════════════════════╗ #
# ║          AUTH CONST          ║ #
# ╚══════════════════════════════╝ #
class JWT_ALGORITHMS(StrEnum):
    HS256 = 'HS256'
    HS384 = 'HS384'
    HS512 = 'HS512'
    RS256 = 'RS256'

class ROLES(StrEnum): # this aren't the passwords, just the role names
    OWNER:      str = 'owner'
    MAINTAINER: str = 'maintain'
    USER:       str = 'user'

# ╔══════════════════════════════╗ #
# ║          HTTP CONST          ║ #
# ╚══════════════════════════════╝ #
@dataclass(frozen=True)
class http_verbs:
    GET:        Const[str] = 'GET'
    POST:       Const[str] = 'POST'
    PUT:        Const[str] = 'PUT'
    PATCH:      Const[str] = 'PATCH'
    DELETE:     Const[str] = 'DELETE'
    OPTIONS:    Const[str] = 'OPTIONS'
    HEAD:       Const[str] = 'HEAD'
    
    ALL_:       Const[str] = f'{GET},{HEAD},{POST},{PUT},{PATCH},{DELETE},{OPTIONS}'
    CLASIC_:    Const[str] = f'{GET},{POST},{PUT},{DELETE}'
    SAFE_:      Const[str] = f'{GET},{HEAD},{OPTIONS}'
    GETTERS_:   Const[str] = f'{GET},{HEAD}'
    ADDERS_:    Const[str] = f'{POST},{PUT},{PATCH}'
    SETTERS_:   Const[str] = f'{PUT},{PATCH}'
    REMOVERS_:  Const[str] = f'{DELETE}'