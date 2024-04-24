from fastapi import APIRouter
from fastapi.responses import JSONResponse
from config.dbconnection import session
from models.estados import Estados
from models.vehiculos import Vehiculos
from models.propietarios import Propietarios
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
  vehiculos = db.query(Vehiculos).all()
  return JSONResponse(content=jsonable_encoder(vehiculos))

@reports_router.get('/propietarios')
async def get_propietarios():
  db = session()
  propietarios = db.query(Propietarios).all()
  return JSONResponse(content=jsonable_encoder(propietarios))