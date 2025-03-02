from pydantic import BaseModel

class NewMeasRequest(BaseModel):
    patEmail: str
