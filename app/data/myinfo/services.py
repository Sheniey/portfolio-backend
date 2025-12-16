
from typing import Optional

from app.core.types import Language
from app.core.db import myinfo_collection as MYINFO
from app.core.consts import DEFAULT_LANGUAGE
from app.utils.i18n import translate
from app.data.myinfo.models import MyInfoOut
from app.data.myinfo.types import myinfo_t
from app.data.myinfo.errors import InvalidInfoObject, InfoNotFoundError, AttributeNotFound

# ╔══════════════════════════════╗ #
# ║           FEATURES           ║ #
# ╚══════════════════════════════╝ #
def __dumper__(info: myinfo_t, lang: Language = DEFAULT_LANGUAGE, *, path: Optional[str] = None) -> MyInfoOut:
    payload: myinfo_t

    try:
        payload = info.copy()
    except:
        raise InvalidInfoObject(info, path=path).throw()

    translate(payload, lang,
        'about_me'
    )
    
    return MyInfoOut(**payload)

def get_myinfo(lang: Language = DEFAULT_LANGUAGE, *, path: Optional[str] = None) -> MyInfoOut:
    payload: myinfo_t | None = MYINFO.find_one({})
    
    if not payload:
        raise InfoNotFoundError(path).throw()
    
    return __dumper__(payload, lang, path=path)

def edit_myinfo(info: myinfo_t, *, path: Optional[str] = None) -> None:
    try:
        MYINFO.update_one({}, {'$set': info}, upsert=True)
    except:
        raise InvalidInfoObject(info, path=path).throw()
    
    return

def delete_attr(attr: str, *, path: Optional[str] = None) -> None:
    try:
        MYINFO.update_one({}, {'$unset': {attr: ''}})
    except:
        raise AttributeNotFound(attr, path=path).throw()
    
    return

def delete_everything(*, path: Optional[str] = None) -> None:
    try:
        MYINFO.delete_many({})
    except:
        raise InfoNotFoundError(path).throw()
    
    return
