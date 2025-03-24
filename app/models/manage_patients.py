from pydantic import BaseModel, EmailStr, constr
from typing import Optional, Dict

from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field
from datetime import date

# Dati anagrafici
class PersonalInfo(BaseModel):
    nome: str
    cognome: str
    dob: date = Field(..., description="Data di nascita")
    indirizzo: Optional[str] = ""
    professione: Optional[str] = ""
    email: EmailStr
    phone: str = Field(..., description="Numero di telefono")
    codice_fiscale: Optional[str] = ""
    come_conosciuto: Optional[str] = Field(None, description="Come hai conosciuto lo studio")
    motivo_visita: str

# Storia ponderale
class WeightHistory(BaseModel):
    peso_attuale: float
    peso_medio: Optional[float] = None
    peso_massimo: Optional[float] = None
    peso_minimo: Optional[float] = None
    fluttuazioni_peso: Optional[str] = None
    percezione_peso: Optional[str] = None
    accumulo_peso: Optional[str] = None

# Relazione con il peso e le diete
class DietHistory(BaseModel):
    diete_precedenti: Optional[str] = None
    difficolta_mantenimento_peso: Optional[str] = None
    aspettative_dieta: Optional[str] = None

# Stile di vita e attività fisica
class Lifestyle(BaseModel):
    lavoro: Optional[str] = None
    ore_lavoro_giorno: Optional[int] = None
    turnista: Optional[bool] = None
    routine_lavorativa: Optional[str] = None
    attivita_fisica: Optional[str] = None

# Abitudini alimentari
class EatingHabits(BaseModel):
    pasti_giornata_tipo: Optional[str] = None
    orari_frequenza_pasti: Optional[str] = None
    problemi_controllo_fame: Optional[str] = None

# Integrazione e farmaci
class SupplementsAndDrugs(BaseModel):
    integratori: Optional[str] = None
    proteine_polvere: Optional[bool] = None
    farmaci: Optional[str] = None
    dosaggi: Optional[str] = None

# Salute intestinale
class GutHealth(BaseModel):
    problemi_digestivi: Optional[str] = None
    regolarita_intestinale: Optional[str] = None
    alimenti_gonfiore: Optional[str] = None

# Stato dello stomaco
class StomachHealth(BaseModel):
    problemi_gastrointestinali: Optional[str] = None
    alimenti_fastidio: Optional[str] = None

# Settore donna
class WomenHealth(BaseModel):
    ciclo_regolare: Optional[bool] = None
    dolori_mestruali: Optional[bool] = None
    sindrome_premestruale: Optional[bool] = None
    cistiti_infezioni: Optional[bool] = None
    gravidanza: Optional[bool] = None

# Patologie e storia familiare
class MedicalHistory(BaseModel):
    patologie: Optional[str] = None
    allergie: Optional[str] = None
    storia_familiare: Optional[str] = None

# Abitudini alimentari e preferenze
class FoodPreferences(BaseModel):
    cibi_non_graditi: Optional[str] = None
    comfort_food: Optional[str] = None
    pasti_fuori_casa_frequenza: Optional[str] = None

# Fumo, sonno e stress
class SmokingSleepStress(BaseModel):
    fumo: Optional[str] = None
    qualita_sonno: Optional[str] = None
    ore_sonno: Optional[int] = None
    livello_stress: Optional[str] = None
    fonti_stress: Optional[str] = None
    gestione_stress: Optional[str] = None

class NewPatientProfile(BaseModel):
    personal_info: PersonalInfo
    weight_history: WeightHistory
    diet_history: DietHistory
    lifestyle: Lifestyle
    eating_habits: EatingHabits
    supplements_and_drugs: SupplementsAndDrugs
    gut_health: GutHealth
    stomach_health: StomachHealth
    women_health: Optional[WomenHealth] = None  # opzionale per uomini
    medical_history: MedicalHistory
    food_preferences: FoodPreferences
    smoking_sleep_stress: SmokingSleepStress
    
class NewMeasRequest(BaseModel):
    patId: str