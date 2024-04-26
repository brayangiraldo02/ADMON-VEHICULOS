from fastapi import APIRouter
from fastapi.responses import JSONResponse
from config.dbconnection import session
from models.estados import Estados
from models.vehiculos import Vehiculos
from models.propietarios import Propietarios
from models.conductores import Conductores
from fastapi.encoders import jsonable_encoder

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

@reports_router.get('/vehiculos-estados')
async def get_vehiculos_estados():
  db = session()
  try:
    vehiculos_estados = db.query(Estados.CODIGO, Estados.NOMBRE, Vehiculos.PLACA) \
    .join(Vehiculos, Estados.CODIGO == Vehiculos.ESTADO) \
    .all()
    vehiculos_estados_list = [{'codigo': vehiculo.CODIGO, 'nombre': vehiculo.NOMBRE, 'placa': vehiculo.PLACA} for vehiculo in vehiculos_estados]
    return JSONResponse(content=jsonable_encoder(vehiculos_estados_list))
  finally:
    db.close()

@reports_router.get('/vehiculos-detalles')
async def get_vehiculos_detalles():
    db = session()
    try:
      vehiculos_detalles = db.query(
        Propietarios.CODIGO,
        Propietarios.ABREVIADO,
        Estados.CODIGO,
        Estados.NOMBRE,
        Vehiculos.NUMERO,
        Vehiculos.PLACA,
        Vehiculos.NOMMARCA,
        Vehiculos.MODELO,
        Vehiculos.LINEA,
        Vehiculos.NRO_CUPO,
        Vehiculos.CHASISNRO,
        Conductores.NROENTREGA,
        Conductores.CUO_DIARIA,
        Conductores.NROENTSDO,
        Conductores.CODIGO,
        Conductores.NOMBRE,
        Conductores.CEDULA,
        Conductores.TELEFONO
      ).join(Vehiculos, Estados.CODIGO == Vehiculos.ESTADO) \
      .join(Conductores, Vehiculos.CONDUCTOR == Conductores.CODIGO) \
      .join(Propietarios, Vehiculos.PROPI_IDEN == Propietarios.CODIGO) \
      .filter(Estados.CODIGO == '01') \
      .all()
      vehiculos_detalles_list = [dict(row) for row in vehiculos_detalles]
      return JSONResponse(content=jsonable_encoder(vehiculos_detalles_list))
    finally:
        db.close()

@reports_router.get('/propietarios')
async def get_propietarios():
  db = session()
  propietarios = db.query(Propietarios).all()
  return JSONResponse(content=jsonable_encoder(propietarios))