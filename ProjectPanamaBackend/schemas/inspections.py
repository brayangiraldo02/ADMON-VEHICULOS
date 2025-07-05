from pydantic import BaseModel

class InspectionInfo(BaseModel):
  propietario: str
  conductor: str
  vehiculo: str
  fechaInicial: str
  fechaFinal: str