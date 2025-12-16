
from typing import Optional, Any
from functools import lru_cache

from app.core.consts import DEFAULT_LANGUAGE
from app.core.types import T, Translations, Language
from app.core.errors import TranslationNotAvailable
from app.utils.cache_tools import cached

__all__ = [
    'use_translation',
    'translate',
]

# ╔══════════════════════════════╗ #
# ║      TRANSLATION HOOKS       ║ #
# ╚══════════════════════════════╝ #
@cached(48, diff_types=True)
def use_translation(element: Translations[T], lang: Language = DEFAULT_LANGUAGE, *, path: Optional[str] = None) -> T:
    '''
    Obtiene la traducción de un elemento traducible basado en el lenguaje solicitado.\n
    `NOTE: Esta función no modifica el objeto original, si desea modificarlo use la función translate().`
    
    :param element: Elemento|Llave para traducir.
    :type element: Translations[T]
    :param lang: Lenguaje al cual traducir.
    :type lang: Language
    :param path: Ruta de la URL para mostrar en caso de error.
    :type path: Optional[str]
    
    :return: Devuelve la traducción obtenida.
    :rtype: T
    '''
    translation: T | None = element.get(lang, element.get(DEFAULT_LANGUAGE, None))
    
    if translation is None:
        raise TranslationNotAvailable(
            element=element,
            requested_lang=lang,
            default_lang=DEFAULT_LANGUAGE,
            path=path,
        )
    
    return translation


# ╔══════════════════════════════╗ #
# ║      TRANSLATION UTILS       ║ #
# ╚══════════════════════════════╝ #
def translate(obj: dict[str, T], lang: Language, *keys: str, path: Optional[str] = None) -> dict[str, T]:
    '''
    Traduce los campos especificados de un objeto dado si contienen traducciones por un lenguaje en especifico.\n
    `NOTE: Esta función modifica el objeto original.`
    
    :param obj: Objeto a iterar para traducir directamente.
    :type obj: dict[str, T]
    :param lang: Lenguaje al cual traducir.
    :type lang: Language
    :param keys: Llaves del objeto para traducir.
    :type keys: str
    :param path: Ruta de la URL para mostrar en caso de error.
    :type path: Optional[str]
    
    :return: Devuelve un diccionario con las traducciones aplicadas.
    :rtype: dict[str, T]
    '''
    applied: dict[str, T] = {}

    for key in keys:
        value: T = obj.get(key)

        if isinstance(value, dict) and ('en' in value or 'es' in value):
            translated = use_translation(value, lang, path=path)
            obj[key] = translated
            applied[key] = translated
            print(applied, key, value)
            continue

        applied[key] = value
    return applied