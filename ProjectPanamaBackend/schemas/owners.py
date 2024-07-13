from pydantic import BaseModel
from typing import Optional

class PropietarioUpdate(BaseModel):
    nombre_propietario: Optional[str] = None
    nombre_abreviado: Optional[str] = None
    nit: Optional[int] = None
    cnt: Optional[str] = None
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
    impuesto: Optional[int] = None
    admon_parado: Optional[int] = None
    descuento: Optional[int] = None
    razon_social: Optional[str] = None
    representante: Optional[str] = None
    tipo_documento: Optional[str] = None
    numero_documento: Optional[str] = None
    sexo: Optional[str] = None
    estado_civil: Optional[str] = None
    nacionalidad: Optional[str] = None
    ficha: Optional[str] = None
    documento: Optional[str] = None
    fec_ingreso: Optional[str] = None
    fec_nacimiento: Optional[str] = None

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
    razon_social: str
    representante: str
    tipo_documento: str
    numero_documento: str
    sexo: str
    estado_civil: str
    nacionalidad: str
    ficha: str
    documento: str
    
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