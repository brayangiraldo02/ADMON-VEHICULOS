from fastapi import APIRouter
from fastapi.responses import JSONResponse
from config.dbconnection import session
from models.estados import Estados
from models.vehiculos import Vehiculos
from models.propietarios import Propietarios
from models.conductores import Conductores
from fastapi.encoders import jsonable_encoder
from schemas.forms import *

reports_router = APIRouter()

@reports_router.get('/estados')
async def get_estados():
  db = session()
  estados = db.query(Estados).all()
  return JSONResponse(content=jsonable_encoder(estados))

@reports_router.get('/vehiculos')
async def get_vehiculos():
  db = session()
  try:
    vehiculos = db.query(Vehiculos.PLACA).all()
    vehiculos_placas = [{'placa': placa[0]} for placa in vehiculos]
    return JSONResponse(content=jsonable_encoder(vehiculos_placas))
  finally:
    db.close()

@reports_router.get('/conteo-vehiculos-estados')
async def get_conteo_vehiculos_estados():
  db = session()
  try:
    conteo_vehiculos_estados = db.query(Estados.CODIGO, Estados.NOMBRE, Vehiculos.PLACA) \
    .join(Vehiculos, Estados.CODIGO == Vehiculos.ESTADO) \
    .all()
    vehiculos_estados_list = [{'codigo': vehiculo.CODIGO, 'nombre': vehiculo.NOMBRE, 'placa': vehiculo.PLACA} for vehiculo in conteo_vehiculos_estados]
    fun_conteo_vehiculos_estados(vehiculos_estados_list)
    return JSONResponse(content=jsonable_encoder(fun_conteo_vehiculos_estados(vehiculos_estados_list)))
  finally:
    db.close()

@reports_router.get('/conteo-propietarios-vehiculos-estados')
async def get_conteo_propietarios_vehiculos_estados():
  db = session()
  try:
    conteo_propietarios_vehiculos_estados = db.query(Propietarios.ABREVIADO, Estados.CODIGO, Estados.NOMBRE, Vehiculos.PLACA) \
    .join(Vehiculos, Estados.CODIGO == Vehiculos.ESTADO) \
    .join(Propietarios, Vehiculos.PROPI_IDEN == Propietarios.CODIGO) \
    .all()
    vehiculos_estados_propietarios_list = [{'empresa': vehiculo.ABREVIADO, 'codigo': vehiculo.CODIGO, 'nombre': vehiculo.NOMBRE, 'placa': vehiculo.PLACA} for vehiculo in conteo_propietarios_vehiculos_estados]
    result = obtener_conteo_por_propietario(vehiculos_estados_propietarios_list)
    return JSONResponse(content=jsonable_encoder(result))
  finally:
    db.close()

@reports_router.get('/vehiculos-detalles')
async def get_vehiculos_detalles():
    db = session()
    try:
        vehiculos_detalles = db.query(
            Propietarios.CODIGO.label('propietario_codigo'),
            Propietarios.ABREVIADO.label('propietario_abreviado'),
            Estados.CODIGO.label('estado_codigo'),
            Estados.NOMBRE.label('estado_nombre'),
            Vehiculos.NUMERO.label('vehiculo_numero'),
            Vehiculos.PLACA.label('vehiculo_placa'),
            Vehiculos.NOMMARCA.label('vehiculo_marca'),
            Vehiculos.MODELO.label('vehiculo_modelo'),
            Vehiculos.LINEA.label('vehiculo_linea'),
            Vehiculos.NRO_CUPO.label('vehiculo_nro_cupo'),
            Vehiculos.CHASISNRO.label('vehiculo_chasis'),
            Conductores.NROENTREGA.label('conductor_nro_entrega'),
            Conductores.CUO_DIARIA.label('conductor_cuo_diaria'),
            Conductores.NROENTSDO.label('conductor_nro_ent_sdo'),
            Conductores.CODIGO.label('conductor_codigo'),
            Conductores.NOMBRE.label('conductor_nombre'),
            Conductores.CEDULA.label('conductor_cedula'),
            Conductores.TELEFONO.label('conductor_telefono')
        )   .join(Vehiculos, Estados.CODIGO == Vehiculos.ESTADO) \
            .join(Conductores, Vehiculos.CONDUCTOR == Conductores.CODIGO) \
            .join(Propietarios, Vehiculos.PROPI_IDEN == Propietarios.CODIGO) \
            .filter(Estados.CODIGO == '01') \
            .all()
        
        # Convertir los resultados en un formato JSON
        vehiculos_detalles_list = []
        for resultado in vehiculos_detalles:
            vehiculo_detalle = {
                'propietario_codigo': resultado.propietario_codigo,
                'propietario_abreviado': resultado.propietario_abreviado,
                'estado_codigo': resultado.estado_codigo,
                'estado_nombre': resultado.estado_nombre,
                'vehiculo_numero': resultado.vehiculo_numero,
                'vehiculo_placa': resultado.vehiculo_placa,
                'vehiculo_marca': resultado.vehiculo_marca,
                'vehiculo_modelo': resultado.vehiculo_modelo,
                'vehiculo_linea': resultado.vehiculo_linea,
                'vehiculo_nro_cupo': resultado.vehiculo_nro_cupo,
                'vehiculo_chasis': resultado.vehiculo_chasis,
                'conductor_nro_entrega': resultado.conductor_nro_entrega,
                'conductor_cuo_diaria': resultado.conductor_cuo_diaria,
                'conductor_nro_ent_sdo': resultado.conductor_nro_ent_sdo,
                'conductor_codigo': resultado.conductor_codigo,
                'conductor_nombre': resultado.conductor_nombre,
                'conductor_cedula': resultado.conductor_cedula,
                'conductor_telefono': resultado.conductor_telefono
            }
            vehiculos_detalles_list.append(vehiculo_detalle)
        
        return JSONResponse(content=jsonable_encoder(vehiculos_detalles_list))
    finally:
        db.close()


@reports_router.get('/propietarios')
async def get_propietarios():
  db = session()
  propietarios = db.query(Propietarios).all()
  return JSONResponse(content=jsonable_encoder(propietarios))