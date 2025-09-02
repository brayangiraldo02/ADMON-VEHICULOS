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
  extintor: bool
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
  pago_mnicipio: bool
  formato_colisiones_menores: bool
  poliza_seguros: bool
  luces_delanteras: bool
  luces_traseras: bool
  vidrios: bool
  retrovisor: bool
  tapiceria: bool
  gps: bool
  combustible: bool #! En el formulario aparece como cuadro de texto, en la base de datos como booleano
  panapass: bool #! En el formulario aparece como cuadro de texto, en la base de datos como booleano
  description: str
  photo1: str
  photo2: str
  photo3: str
  photo4: str
  photo5: str
  photo6: str
  photo7: str
  photo8: str
  photo9: str
  photo10: str
  photo11: str
  photo12: str
  photo13: str
  photo14: str
  photo15: str
  photo16: str