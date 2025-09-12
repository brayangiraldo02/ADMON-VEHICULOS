from typing import Optional
from pydantic import BaseModel

class InspectionInfo(BaseModel):
  usuario: Optional[str] = None
  propietario: str
  conductor: str
  vehiculo: str
  fechaInicial: str
  fechaFinal: str

class NewInspection(BaseModel):
  user: str
  company_code: str
  vehicle_number: str
  mileage: int
  inspection_type: str
  inspection_date: str
  inspection_time: str
  alfombra: bool
  copas_rines: bool
  extinguidor: bool
  antena: bool
  lamparas: bool
  triangulo: bool
  gato: bool
  pipa: bool
  copas: bool
  llanta_repuesto: bool
  placa_municipal: bool
  caratula_radio: bool
  registro_vehiculo: bool
  revisado: bool
  pago_municipio: bool
  formato_colisiones_menores: bool
  poliza_seguros: bool
  luces_delanteras: bool
  luces_traseras: bool
  vidrios: bool
  retrovisor: bool
  tapiceria: bool
  gps: bool
  combustible: str #! En el formulario aparece como cuadro de texto, en la base de datos como booleano
  panapass: str #! En el formulario aparece como cuadro de texto, en la base de datos como booleano
  description: str