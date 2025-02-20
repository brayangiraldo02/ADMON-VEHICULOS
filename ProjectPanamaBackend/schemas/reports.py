from pydantic import BaseModel
from typing import List

class userInfo(BaseModel):
  user: str

class infoReports(BaseModel):
  usuario: str
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