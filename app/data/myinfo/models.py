
from pydantic import BaseModel, Field

from app.core.types import Email, Translations
from app.data.myinfo.consts import DEFAULT_BIRTH, DEFAULT_EMAIL, DEFAULT_LOCATION

"""
{
    "full_name": "José Daniel Ávalos Becerra",
    "first_name": "José Daniel",
    "last_name": "Ávalos Becerra",
    "pseudonym": "Sheñey",
    "pseudonym_ascii": "Sheney",
    "about_me": "Soy un estudiante de secundaria apasionado por la tecnología y la programación. Me encanta aprender cosas nuevas y enfrentar desafíos que me permitan crecer tanto personal como académicamente. En mi tiempo libre, disfruto explorando nuevas tecnologías, jugando videojuegos y pasando tiempo con mis amigos y familia.",
    "phone": "3171119640",
    "email": "sheneyby2010@gmail.com",
    "emails": [
        {
            "name": "sheneyby2010",
            "domain": "gmail.com",
            "primary": true
        },
        {
            "name": "joseda.avalosbe",
            "domain": "gmail.com",
            "primary": false
        },
        {
            "name": "joseda.avalosbe",
            "domain": "outlook.com",
            "primary": false
        },
        {
            "name": "jose.avalos1862",
            "domain": "alumnos.udg.mx",
            "primary": false
        }
    ],
    "location": "Autlán de Navarro, Jalisco, México",
    "born_date": "2010-09-08"
}"""

# ╔══════════════════════════════╗ #
# ║        CONTENT MODELS        ║ #
# ╚══════════════════════════════╝ #
class MyInfoIn(BaseModel):
    full_name: str              = Field(..., description='Full name of the person')
    first_name: str             = Field(..., description='First name of the person')
    last_name: str              = Field(..., description='Last name of the person')
    pseudonym: str              = Field(..., description='Pseudonym or nickname of the person')
    pseudonym_ascii: str        = Field(..., description='ASCII-7 version of the pseudonym')
    about_me: Translations[str] = Field(..., description='Short biography about the person')
    phone: str                  = Field(..., description='Phone number of the person')
    email: str                  = Field(DEFAULT_EMAIL, description='Primary email address of the person')
    emails: list[Email]         = Field(..., description='List of email addresses associated with the person')
    location: str               = Field(DEFAULT_LOCATION, description='Location of the person')
    born_date: str              = Field(DEFAULT_BIRTH, description='Birth date of the person in YYYY-MM-DD format')

class MyInfoOut(BaseModel):
    full_name: str              = Field(..., description='Full name of the person')
    first_name: str             = Field(..., description='First name of the person')
    last_name: str              = Field(..., description='Last name of the person')
    pseudonym: str              = Field(..., description='Pseudonym or nickname of the person')
    pseudonym_ascii: str        = Field(..., description='ASCII-7 version of the pseudonym')
    about_me: str               = Field(..., description='Short biography about the person')
    phone: str                  = Field(..., description='Phone number of the person')
    email: str                  = Field(DEFAULT_EMAIL, description='Primary email address of the person')
    emails: list[Email]         = Field(..., description='List of email addresses associated with the person')
    location: str               = Field(DEFAULT_LOCATION, description='Location of the person')
    born_date: str              = Field(DEFAULT_BIRTH, description='Birth date of the person in YYYY-MM-DD format')
