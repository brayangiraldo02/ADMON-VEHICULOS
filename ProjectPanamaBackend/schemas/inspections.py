from pydantic import BaseModel

class InspectionInfo(BaseModel):
  propietario: str
  conductor: str
  vehiculo: str
  primeraFecha: str
  ultimaFecha: str