from pydantic import BaseModel
from typing import List, Optional

class userInfo(BaseModel):
  user: str

class infoReports(BaseModel):
  usuario: str
  empresa: Optional[str] = None
  empresas: List[str]
  estados: List[str]

class PartsRelationshipReport(BaseModel):
  usuario: str
  primeraFecha: str
  ultimaFecha: str
  unidad: str
  empresa: str

class RelationshipRevenuesReport(BaseModel):
  usuario: str
  primeraFecha: str
  ultimaFecha: str
  unidad: str
  empresa: str

class PandGStatusReport(BaseModel):
  usuario: str
  primeraFecha: str
  ultimaFecha: str
  unidad: str
  empresa: str