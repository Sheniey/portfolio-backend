
from typing import Literal, Optional, Callable, TypeVar, ParamSpec, TypedDict, Generic

__all__ = [
    'T', 'P', 'R', 'F',
    'Languages', 'Translations',
    'Email',
]

# ╔══════════════════════════════╗ #
# ║        GENERIC TYPES         ║ #
# ╚══════════════════════════════╝ #
T = TypeVar('T')   # Generic Type

P = ParamSpec('P') # Parameter Specification
R = TypeVar('R')   # Return Type
F = Callable[P, R] # Function Type

type Language = Literal['en', 'es']

# ╔══════════════════════════════╗ #
# ║       GLOBAL STRUCTS         ║ #
# ╚══════════════════════════════╝ #
class Translations(TypedDict, Generic[T]):
    en: T
    es: T

class Email(TypedDict):
    name: str
    domain: str
    primary: bool

