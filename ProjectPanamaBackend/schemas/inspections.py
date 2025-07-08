from typing import Optional
from pydantic import BaseModel

class InspectionInfo(BaseModel):
  usuario: Optional[str] = None
  propietario: str
  conductor: str
  vehiculo: str
  fechaInicial: str
  fechaFinal: str