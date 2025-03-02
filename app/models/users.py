from pydantic import BaseModel, EmailStr, constr
from typing import Optional

class NewPatientProfile(BaseModel):
    nome: str
    cognome: str
    email: EmailStr
    phone: str
    indirizzo: Optional[str] = ""
    altezza: int
    peso: int
    dob: str
    genere: str
    patologie: Optional[str] = ""
    allergie: Optional[str] = ""
    terapie: Optional[str] = ""
    lev_activity: str
    alim_pref: Optional[str] = ""
    alim_intolleranze: Optional[str] = ""