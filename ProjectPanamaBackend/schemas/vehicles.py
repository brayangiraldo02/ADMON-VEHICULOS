from pydantic import BaseModel
from typing import Optional

class VehicleUpdate(BaseModel):
    vehiculo_numero: Optional[int] = None
    vehiculo_placa: Optional[str] = None
    vehiculo_modelo: Optional[str] = None
    vehiculo_nro_cupo: Optional[int] = None
    vehiculo_permiso_nro: Optional[str] = None
    vehiculo_motor: Optional[str] = None
    vehiculo_chasis: Optional[str] = None
    vehiculo_fec_matricula: Optional[str] = None
    vehiculo_empresa: Optional[str] = None
    vehiculo_conductor: Optional[str] = None
    vehiculo_estado: Optional[str] = None
    vehiculo_cuota_diaria: Optional[float] = None
    vehiculo_nro_Ctas: Optional[int] = None
    vehiculo_panapass: Optional[str] = None
    vehiculo_panapass_pwd: Optional[str] = None
    vehiculo_sdo_panapa: Optional[float] = None

    