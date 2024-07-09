from pydantic import BaseModel
from typing import Optional

class PropietarioUpdate(BaseModel):
    nombre: Optional[str] = None
    abreviado: Optional[str] = None
    cc: Optional[str] = None
    ruc: Optional[str] = None
    ciudad: Optional[str] = None
    direccion: Optional[str] = None
    telefono: Optional[str] = None
    celular: Optional[str] = None
    celular1: Optional[str] = None
    representante: Optional[str] = None
    contacto: Optional[str] = None
    correo: Optional[str] = None
    correo1: Optional[str] = None
    central: Optional[str] = None
    auditor: Optional[str] = None
    stateEdited: Optional[bool] = False
    estado: Optional[str] = None
    grupo: Optional[str] = None
    impuesto: Optional[str] = None
    admon_parado: Optional[str] = None
    descuento: Optional[str] = None

class PropietarioCreate(BaseModel):
    codigo: str
    nombre: str
    abreviado: str
    cc: str
    ruc: str
    auditora: str
    ciudad: str
    direccion: str
    central: str
    telefono: str
    celular: str
    celular1: str
    representante: str
    contacto: str
    correo: str
    correo1: str
    estado: str
    
class RepresentantePropietario(BaseModel):
    razon_social: Optional[str] = None
    representante: Optional[str] = None
    tipo_documento: Optional[str] = None
    numero_documento: Optional[str] = None
    sexo: Optional[str] = None
    estado_civil: Optional[str] = None
    nacionalidad: Optional[str] = None
    ficha: Optional[str] = None
    documento: Optional[str] = None
