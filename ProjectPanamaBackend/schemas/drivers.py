from pydantic import BaseModel
from typing import Optional

class ConductorUpdate(BaseModel):
  nombre: Optional[str] = None
  apellido: Optional[str] = None
  cedula: Optional[str] = None
  licencia_numero: Optional[str] = None
  licencia_categoria: Optional[str] = None
  licencia_vencimiento: Optional[str] = None
  fecha_nacimiento: Optional[str] = None
  estado_civil: Optional[str] = None
  sexo: Optional[str] = None
  direccion: Optional[str] = None
  detalle: Optional[str] = None
  telefono: Optional[str] = None
  celular: Optional[str] = None
  ciudad: Optional[str] = None
  contacto: Optional[str] = None
  contacto1: Optional[str] = None
  contacto2: Optional[str] = None
  correo: Optional[str] = None
  par_contacto: Optional[str] = None
  par_contacto1: Optional[str] = None
  par_contacto2: Optional[str] = None
  tel_contacto: Optional[str] = None
  tel_contacto1: Optional[str] = None
  tel_contacto2: Optional[str] = None
  representa: Optional[str] = None
  cruce_ahorros: Optional[str] = None
  observaciones: Optional[str] = None
  estado: Optional[str] = None
  fecha_estado: Optional[str] = None
  fecha_ingreso: Optional[str] = None
  fecha_retiro: Optional[str] = None
  stateEdited: Optional[bool] = False

class ConductorCreate(BaseModel):
  codigo: int
  nombre: str
  cedula: int
  ciudad: Optional[str] = ''
  telefono: Optional[str] = ''
  celular: Optional[str] = ''
  correo: Optional[str] = ''
  sexo: Optional[str] = ''
  fecha_ingreso: Optional[str] = ''
  direccion: Optional[str] = ''
  fecha_nacimiento: Optional[str] = ''
  representa: Optional[str] = ''
  estado_civil: Optional[str] = ''
  fecha_retiro: Optional[str] = ''
  contacto: Optional[str] = ''
  contacto1: Optional[str] = ''
  contacto2: Optional[str] = ''
  tel_contacto: Optional[str] = ''
  tel_contacto1: Optional[str] = ''
  tel_contacto2: Optional[str] = ''
  par_contacto: Optional[str] = ''
  par_contacto1: Optional[str] = ''
  par_contacto2: Optional[str] = ''
  estado: Optional[str] = ''
  contrato_auto: Optional[str] = ''
  cruce_ahorros: Optional[str] = ''
  licencia_numero: Optional[str] = ''
  licencia_categoria: Optional[str] = ''
  licencia_vencimiento: Optional[str] = ''
  detalle: Optional[str] = ''
  observaciones: Optional[str] = ''