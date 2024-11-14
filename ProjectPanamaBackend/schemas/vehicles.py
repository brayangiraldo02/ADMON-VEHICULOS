from pydantic import BaseModel, Field
from typing import Optional

class VehicleUpdate(BaseModel):
    stateEdited: bool = Field(default=False)
    vehiculo_admon: int = Field(default=0)
    vehiculo_ahorro_siniestro: int = Field(default=0)
    vehiculo_blindaje: str = Field(default="")
    vehiculo_capacidad: str = Field(default="")
    vehiculo_categoria: str = Field(default="")
    vehiculo_central: str = Field(default="")
    vehiculo_certificado_operacion: str = Field(default="")
    vehiculo_certificado_operacion_fec: str = Field(default="")
    vehiculo_chasis: str = Field(default="")
    vehiculo_chasis_reg: str = Field(default="")
    vehiculo_cilindraje: str = Field(default="")
    vehiculo_clase: str = Field(default="")
    vehiculo_cobro_admon: str = Field(default="")
    vehiculo_codigo_barras: str = Field(default="")
    vehiculo_color: str = Field(default="")
    vehiculo_combustible: str = Field(default="")
    vehiculo_consecutivo: str = Field(default="")
    vehiculo_consulta_panapass: str = Field(default="")
    vehiculo_cta_gasto: str = Field(default="")
    vehiculo_dec_importacion: str = Field(default="")
    vehiculo_extinguidor: str = Field(default="")
    vehiculo_extinguidor_vence: str = Field(default="")
    vehiculo_factura_compra: int = Field(default=0)
    vehiculo_fec_creacion: str = Field(default="")
    vehiculo_fec_estado: str = Field(default="")
    vehiculo_fec_factura_compra: str = Field(default="")
    vehiculo_fec_importacion: str = Field(default="")
    vehiculo_fec_inicio_piquera: str = Field(default="")
    vehiculo_fec_matricula: str = Field(default="")
    vehiculo_fec_modelo: str = Field(default="")
    vehiculo_fec_poliza: str = Field(default="")
    vehiculo_fec_primer_pago: str = Field(default="")
    vehiculo_fec_ultimo_pago: str = Field(default="")
    vehiculo_fec_vencimiento_matricula: str = Field(default="")
    vehiculo_fec_vencimiento_permiso: str = Field(default="")
    vehiculo_forma_pago: str = Field(default="")
    vehiculo_kilometraje: int = Field(default=0)
    vehiculo_lateral: str = Field(default="")
    vehiculo_licencia_fec: str = Field(default="")
    vehiculo_licencia_nro: str = Field(default="")
    vehiculo_limit_propiedad: str = Field(default="")
    vehiculo_mantenimiento: int = Field(default=0)
    vehiculo_marca: str = Field(default="")
    vehiculo_modalidad: str = Field(default="")
    vehiculo_modelo: str = Field(default="")
    vehiculo_motor: str = Field(default="")
    vehiculo_motor_reg: str = Field(default="")
    vehiculo_multa_pago: int = Field(default=0)
    vehiculo_ne: str = Field(default="")
    vehiculo_nro_cupo: str = Field(default="")
    vehiculo_nro_puertas: str = Field(default="")
    vehiculo_nro_total_cuotas: str = Field(default="")
    vehiculo_num_poliza: str = Field(default="")
    vehiculo_numero: str = Field(default="")
    vehiculo_observaciones: str = Field(default="")
    vehiculo_organismo_transito: str = Field(default="")
    vehiculo_pago_domingo: str = Field(default="")
    vehiculo_pago_jueves: str = Field(default="")
    vehiculo_pago_lunes: str = Field(default="")
    vehiculo_pago_martes: str = Field(default="")
    vehiculo_pago_miercoles: str = Field(default="")
    vehiculo_pago_sabado: str = Field(default="")
    vehiculo_pago_viernes: str = Field(default="")
    vehiculo_panapass: str = Field(default="")
    vehiculo_panapass_pwd: str = Field(default="")
    vehiculo_permiso_nro: str = Field(default="")
    vehiculo_picoyplaca_domingo: str = Field(default="")
    vehiculo_picoyplaca_jueves: str = Field(default="")
    vehiculo_picoyplaca_lunes: str = Field(default="")
    vehiculo_picoyplaca_martes: str = Field(default="")
    vehiculo_picoyplaca_miercoles: str = Field(default="")
    vehiculo_picoyplaca_sabado: str = Field(default="")
    vehiculo_picoyplaca_viernes: str = Field(default="")
    vehiculo_piquera: str = Field(default="")
    vehiculo_placa: str = Field(default="")
    vehiculo_placa_particular: str = Field(default="")
    vehiculo_placa_particular_vence: str = Field(default="")
    vehiculo_placa_publica: str = Field(default="")
    vehiculo_placa_publica_vence: str = Field(default="")
    vehiculo_plan_pago: str = Field(default="")
    vehiculo_poliza_responsabilidad_civil: str = Field(default="")
    vehiculo_poliza_responsabilidad_civil_vence: str = Field(default="")
    vehiculo_posicion_llave: str = Field(default="")
    vehiculo_potencia: str = Field(default="")
    vehiculo_prendido_apagado: str = Field(default="")
    vehiculo_primer_mantenimiento: str = Field(default="")
    vehiculo_propietario: str = Field(default="")
    vehiculo_recibo: int = Field(default=0)
    vehiculo_rendimientos_propietario: int = Field(default=0)
    vehiculo_renta_diaria: int = Field(default=0)
    vehiculo_reposicion: int = Field(default=0)
    vehiculo_restriccion_movilidad: str = Field(default="")
    vehiculo_saldo_panapass: str = Field(default="")
    vehiculo_serie: str = Field(default="")
    vehiculo_serie_reg: str = Field(default="")
    vehiculo_servicio: str = Field(default="")
    vehiculo_tipo: str = Field(default="")
    vehiculo_tipo_llave: str = Field(default="")
    vehiculo_ultimo_mantenimiento: str = Field(default="")
    vehiculo_valor_compra: int = Field(default=0)
    vehiculo_vin: str = Field(default="")
    vehiculo_vlr_cuo_diaria: int = Field(default=0)
    vehiculo_vlr_ultimo_pago: int = Field(default=0)


# stateEdited: false
# vehiculo_admon: 0
# vehiculo_ahorro_siniestro: 0
# vehiculo_blindaje: ""
# vehiculo_capacidad: "5"
# vehiculo_categoria: "0"
# vehiculo_central: "01"
# vehiculo_certificado_operacion: ""
# vehiculo_certificado_operacion_fec: "0000-00-00 00:00:00"
# vehiculo_chasis: "KNABE512AET517422"
# vehiculo_chasis_reg: ""
# vehiculo_cilindraje: ""
# vehiculo_clase: ""
# vehiculo_cobro_admon: "2"
# vehiculo_codigo_barras: ""
# vehiculo_color: "AMARILLO"
# vehiculo_combustible: ""
# vehiculo_consecutivo: "0002"
# vehiculo_consulta_panapass: "1"
# vehiculo_cta_gasto: ""
# vehiculo_dec_importacion: ""
# vehiculo_extinguidor: ""
# vehiculo_extinguidor_vence: "0000-00-00 00:00:00"
# vehiculo_factura_compra: 0
# vehiculo_fec_creacion: "2023-10-02T00:00:00"
# vehiculo_fec_estado: "2023-10-09"
# vehiculo_fec_factura_compra: "0000-00-00"
# vehiculo_fec_importacion: "0000-00-00 00:00:00"
# vehiculo_fec_inicio_piquera: "0000-00-00 00:00:00"
# vehiculo_fec_matricula: "0000-00-00 00:00:00"
# vehiculo_fec_modelo: "2014"
# vehiculo_fec_poliza: "0000-00-00"
# vehiculo_fec_primer_pago: "0000-00-00 00:00:00"
# vehiculo_fec_ultimo_pago: "0000-00-00 00:00:00"
# vehiculo_fec_vencimiento_matricula: "0000-00-00 00:00:00"
# vehiculo_fec_vencimiento_permiso: "2024-06-06"
# vehiculo_forma_pago: "0"
# vehiculo_kilometraje: 9
# vehiculo_lateral: "1"
# vehiculo_licencia_fec: "0000-00-00 00:00:00"
# vehiculo_licencia_nro: ""
# vehiculo_limit_propiedad: ""
# vehiculo_mantenimiento: 0
# vehiculo_marca: "02"
# vehiculo_modalidad: ""
# vehiculo_modelo: "Picanto"
# vehiculo_motor: "G4LADP019626"
# vehiculo_motor_reg: ""
# vehiculo_multa_pago: 0
# vehiculo_ne: ""
# vehiculo_nro_cupo: "8T23665"
# vehiculo_nro_puertas: "4"
# vehiculo_nro_total_cuotas: "0"
# vehiculo_num_poliza: ""
# vehiculo_numero: "101"
# vehiculo_observaciones: ""
# vehiculo_organismo_transito: ""
# vehiculo_pago_domingo: "F"
# vehiculo_pago_jueves: "F"
# vehiculo_pago_lunes: "F"
# vehiculo_pago_martes: "F"
# vehiculo_pago_miercoles: "F"
# vehiculo_pago_sabado: "F"
# vehiculo_pago_viernes: "F"
# vehiculo_panapass: "601142"
# vehiculo_panapass_pwd: "kgK)kE8L"
# vehiculo_permiso_nro: "13-00189"
# vehiculo_picoyplaca_domingo: "F"
# vehiculo_picoyplaca_jueves: "F"
# vehiculo_picoyplaca_lunes: "F"
# vehiculo_picoyplaca_martes: "F"
# vehiculo_picoyplaca_miercoles: "F"
# vehiculo_picoyplaca_sabado: "F"
# vehiculo_picoyplaca_viernes: "F"
# vehiculo_piquera: ""
# vehiculo_placa: "AA6404"
# vehiculo_placa_particular: ""
# vehiculo_placa_particular_vence: "2019-05-01"
# vehiculo_placa_publica: ""
# vehiculo_placa_publica_vence: "0000-00-00"
# vehiculo_plan_pago: ""
# vehiculo_poliza_responsabilidad_civil: ""
# vehiculo_poliza_responsabilidad_civil_vence: "0000-00-00 00:00:00"
# vehiculo_posicion_llave: ""
# vehiculo_potencia: ""
# vehiculo_prendido_apagado: "0"
# vehiculo_primer_mantenimiento: "0000-00-00 00:00:00"
# vehiculo_propietario: "26"
# vehiculo_recibo: 0
# vehiculo_rendimientos_propietario: 0
# vehiculo_renta_diaria: 0
# vehiculo_reposicion: 0
# vehiculo_restriccion_movilidad: ""
# vehiculo_saldo_panapass: "-2.75"
# vehiculo_serie: ""
# vehiculo_serie_reg: ""
# vehiculo_servicio: "Taxi"
# vehiculo_tipo: ""
# vehiculo_tipo_llave: "0"
# vehiculo_ultimo_mantenimiento: "0000-00-00 00:00:00"
# vehiculo_valor_compra: 0
# vehiculo_vin: ""
# vehiculo_vlr_cuo_diaria: 0
# vehiculo_vlr_ultimo_pago: 0

#--------------------------------------------------------------------------------

class VehicleCreate(BaseModel):
    vehiculo_numero: str
    vehiculo_placa: str
    vehiculo_consecutivo: str
    vehiculo_marca: Optional[str] = ''
    vehiculo_modelo: Optional[str] = ''
    vehiculo_año: Optional[str] = ''
    vehiculo_cilindraje: Optional[str] = ''
    vehiculo_nro_puertas: Optional[str] = ''
    vehiculo_licencia_nro: Optional[str] = ''
    vehiculo_licencia_fec: Optional[str] = ''
    vehiculo_color: Optional[str] = ''
    vehiculo_servicio: Optional[str] = ''
    vehiculo_fec_matricula: Optional[str] = ''
    vehiculo_fec_vencimiento_matricula: Optional[str] = ''
    vehiculo_fec_importacion: Optional[str] = ''
    vehicul_clase: Optional[str] = ''
    vehiculo_tipo: Optional[str] = ''
    vehiculo_combustible: Optional[str] = ''
    vehiculo_capacidad: Optional[str] = ''
    vehiculo_ne: Optional[str] = ''
    vehiculo_motor: Optional[str] = ''
    vehiculo_motor_reg: Optional[str] = ''
    vehiculo_vin: Optional[str] = ''
    vehiculo_serie: Optional[str] = ''
    vehiculo_serie_reg: Optional[str] = ''
    vehiculo_chasis: Optional[str] = ''
    vehiculo_chasis_reg: Optional[str] = ''
    vehiculo_propietario: Optional[str] = ''
    vehiculo_cta_gasto: Optional[str] = ''
    vehiculo_central: Optional[str] = ''
    vehiculo_fec_creacion: Optional[str] = ''
    vehiculo_nro_cupo: Optional[int] = 0
    vehiculo_permiso_nro: Optional[str] = ''
    vehiculo_fec_vencimiento_permiso: Optional[str] = ''
    vehiculo_blindaje: Optional[str] = ''
    vehiculo_potencia: Optional[str] = ''
    vehiculo_dec_importacion: Optional[str] = ''
    vehiculo_restriccion_movilidad: Optional[str] = ''
    vehiculo_limit_propiedad: Optional[str] = ''
    vehiculo_organismo_transito: Optional[str] = ''
    vehiculo_codigo_barras: Optional[str] = ''
    vehiculo_lateral: Optional[str] = ''
    vehiculo_kilometraje: Optional[str] = ''
    vehiculo_modalidad: Optional[str] = ''
    vehiculo_consulta_panapass: Optional[str] = ''
    vehiculo_panapass: Optional[str] = ''
    vehiculo_panapass_pwd: Optional[str] = ''
    vehiculo_placa_particular: Optional[str] = ''
    vehiculo_placa_particular_vence: Optional[str] = ''
    vehiculo_placa_publica: Optional[str] = ''
    vehiculo_placa_publica_vence: Optional[str] = ''
    vehiculo_poliza_responsabilidad_civil: Optional[str] = ''
    vehiculo_poliza_responsabilidad_civil_vence: Optional[str] = ''
    vehiculo_extinguidor: Optional[str] = ''
    vehiculo_extinguidor_vence: Optional[str] = ''
    vehiculo_certificado_operacion: Optional[str] = ''
    vehiculo_certificado_operacion_fec: Optional[str] = ''
    vehiculo_nro_total_cuotas: Optional[int] = 0
    vehiculo_vlr_cuo_diaria: Optional[float] = 0.0
    vehiculo_renta_diaria: Optional[float] = 0.0
    vehiculo_ahorro_siniestro: Optional[float] = 0.0
    vehiculo_cobro_admon: Optional[str] = ''
    vehiculo_admon: Optional[float] = 0.0
    vehiculo_reposicion: Optional[float] = 0.0
    vehiculo_mantenimiento: Optional[float] = 0.0
    vehiculo_rendimientos_propietario: Optional[float] = 0.0
    vehiculo_lunes: Optional[str] = ''
    vehiculo_martes: Optional[str] = ''
    vehiculo_miercoles: Optional[str] = ''
    vehiculo_jueves: Optional[str] = ''
    vehiculo_viernes: Optional[str] = ''
    vehiculo_sabado: Optional[str] = ''
    vehiculo_domingo: Optional[str] = ''
    vehiculo_pago: Optional[str] = ''
    vehiculo_multa_pago: Optional[str] = ''
    vehiculo_fec_primer_pago: Optional[str] = ''
    vehiculo_fec_ultimo_pago: Optional[str] = ''
    vehiculo_vlr_ultimo_pago: Optional[float] = 0.0
    vehiculo_recibo: Optional[str] = ''
    vehiculo_primer_mantenimiento: Optional[str] = ''
    vehiculo_ultimo_mantenimiento: Optional[str] = ''
    vehiculo_categoria: Optional[str] = ''
    vehiculo_tipo_llave: Optional[str] = ''
    vehiculo_fun_llave: Optional[str] = ''
    vehiculo_posicion_llave: Optional[str] = ''
    vehiculo_fec_estado: Optional[str] = ''
    vehiculo_plan_pago: Optional[str] = ''
    vehiculo_prendido_apagado: Optional[str] = ''
    vehiculo_piquera: Optional[str] = ''
    vehiculo_fec_inicio_piquera: Optional[str] = ''
    vehiculo_factura_compra: Optional[str] = ''
    vehiculo_fec_factura_compra: Optional[str] = ''
    vehiculo_valor_compra: Optional[float] = 0.0
    vehiculo_num_poliza: Optional[str] = ''
    vehiculo_fec_poliza: Optional[str] = ''
    vehiculo_observaciones: Optional[str] = ''
    vehiculo_picoyplaca_lunes: Optional[str] = ''
    vehiculo_picoyplaca_martes: Optional[str] = ''
    vehiculo_picoyplaca_miercoles: Optional[str] = ''
    vehiculo_picoyplaca_jueves: Optional[str] = ''
    vehiculo_picoyplaca_viernes: Optional[str] = ''
    vehiculo_picoyplaca_sabado: Optional[str] = ''
    vehiculo_picoyplaca_domingo: Optional[str] = ''