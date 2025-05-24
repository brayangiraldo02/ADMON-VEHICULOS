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
    codigo: int
    nombre_propietario: str
    nombre_abreviado: Optional[str] = ''
    nit: Optional[str] = ''
    cnt: Optional[str] = ''
    ruc: Optional[str] = ''
    razon_social: Optional[str] = ''
    ciudad: Optional[str] = ''
    direccion: Optional[str] = ''
    telefono: Optional[str] = ''
    celular: Optional[str] = ''
    fec_nacimiento: Optional[str] = ''
    fec_ingreso: Optional[str] = ''
    celular1: Optional[str] = ''
    representante: Optional[str] = ''
    sexo: Optional[str] = ''
    estado_civil: Optional[str] = ''
    tipo_documento: Optional[str] = ''
    numero_documento: Optional[str] = ''
    nacionalidad: Optional[str] = ''
    ficha: Optional[str] = ''
    documento: Optional[str] = ''
    contacto: Optional[str] = ''
    correo: Optional[str] = ''
    correo1: Optional[str] = ''
    estado: Optional[str] = ''
    auditor: Optional[str] = ''
    central: Optional[str] = ''
    grupo: Optional[str] = ''
    impuesto: Optional[int] = 0
    descuento: Optional[int] = 0
    admon_parado: Optional[int] = 0


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

class Owner(BaseModel):
    propietario: str

class OwnersList(BaseModel):
    owners: list[str]