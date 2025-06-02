from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from config.dbconnection import session
from sqlalchemy.orm import aliased
from models.conductores import Conductores
from models.vehiculos import Vehiculos
from models.marcas import Marcas
from models.propietarios import Propietarios
from models.estados import Estados
from schemas.operations import *
from middlewares.JWTBearer import JWTBearer
from fastapi.encoders import jsonable_encoder
from utils.reports import *
from datetime import datetime
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
import jinja2
from utils.pdf import html2pdf

operations_router = APIRouter()

@operations_router.get("/operations/deliveryvehicledriver/vehicle/{vehicle_number}/", tags=["Operations"])
async def get_vehicle_operations(vehicle_number: str):
  db = session()
  try:
    vehicle_operations = db.query(
      Marcas.NOMBRE.label('MARCA'), Vehiculos.PLACA, Vehiculos.NRO_CUPO,
      Vehiculos.NROENTREGA, Vehiculos.CUO_DIARIA, Vehiculos.ESTADO, 
      Estados.NOMBRE.label('NOMBRE_ESTADO'), Vehiculos.PROPI_IDEN, 
      Propietarios.NOMBRE.label('NOMBRE_PROPI'), Vehiculos.CONDUCTOR,
      Vehiculos.CON_CUPO, Vehiculos.FEC_ESTADO
    ).join(
      Vehiculos, Vehiculos.MARCA == Marcas.CODIGO
    ).join(
      Estados, Vehiculos.ESTADO == Estados.CODIGO
    ).join(
      Propietarios, Vehiculos.PROPI_IDEN == Propietarios.CODIGO
    ).filter(
      Vehiculos.NUMERO == vehicle_number
    ).first()

    if not vehicle_operations:
      return JSONResponse(content={"error": "Vehicle not found"}, status_code=404)
    
    vehicle = {
      'numero': vehicle_number,
      'marca': vehicle_operations.MARCA,
      'placa': vehicle_operations.PLACA,
      'cupo': vehicle_operations.NRO_CUPO,
      'nro_entrega': vehicle_operations.NROENTREGA,
      'cuota_diaria': vehicle_operations.CUO_DIARIA,
      'estado': vehicle_operations.ESTADO + ' - ' + vehicle_operations.NOMBRE_ESTADO,
      'propietario': vehicle_operations.PROPI_IDEN + ' - ' + vehicle_operations.NOMBRE_PROPI,
      'conductor': vehicle_operations.CONDUCTOR,
      'con_cupo': vehicle_operations.CON_CUPO,
      'fecha_estado': vehicle_operations.FEC_ESTADO
    }

    return JSONResponse(content=jsonable_encoder(vehicle), status_code=200)
  
  except Exception as e:
    return JSONResponse(content={"error": str(e)}, status_code=500)
  
  finally:
    db.close()

@operations_router.get("/operations/deliveryvehicledriver/driver/{driver_number}/", tags=["Operations"])
async def get_driver_operations(driver_number: str):
  db = session()
  try:
    driver_operations = db.query(
      Conductores.NOMBRE, Conductores.CEDULA, Conductores.TELEFONO, 
      Conductores.CELULAR, Conductores.DIRECCION, Conductores.LICEN_NRO, 
      Conductores.LICEN_VCE, Conductores.UND_NRO, Conductores.ESTADO
    ).filter(
      Conductores.CODIGO == driver_number
    ).first()

    if not driver_operations:
      return JSONResponse(content={"error": "Driver not found"}, status_code=404)
    
    driver = {
      'codigo': driver_number,
      'nombre': driver_operations.NOMBRE,
      'cedula': driver_operations.CEDULA,
      'telefono': driver_operations.TELEFONO + ' | ' + driver_operations.CELULAR,
      'direccion': driver_operations.DIRECCION,
      'licencia_numero': driver_operations.LICEN_NRO,
      'licencia_vencimiento': driver_operations.LICEN_VCE,
      'vehiculo': driver_operations.UND_NRO,
      'estado': driver_operations.ESTADO
    }

    return JSONResponse(content=jsonable_encoder(driver), status_code=200)
  
  except Exception as e:
    return JSONResponse(content={"error": str(e)}, status_code=500)
  
  finally:
    db.close()

@operations_router.post("/operations/deliveryvehicledriver/", tags=["Operations"])
async def delivery_vehicle_driver(data: DeliveryVehicleDriver):
  db = session()
  try:
    vehicle = db.query(Vehiculos).filter(Vehiculos.NUMERO == data.vehicle_number).first()
    if not vehicle:
      return JSONResponse(content={"error": "Vehicle not found"}, status_code=404)
    
    driver = db.query(Conductores).filter(Conductores.CODIGO == data.driver_number).first()
    if not driver:
      return JSONResponse(content={"error": "Driver not found"}, status_code=404)
    
    if(driver.ESTADO != '1' and 
       driver.UND_NRO != '' and 
       vehicle.ESTADO != '06' and 
       vehicle.CON_CUPO != 1 and
       vehicle.CONDUCTOR != ''):
      return JSONResponse(content={"error": "Driver already has a vehicle assigned"}, status_code=400)
    
    vehicle.CONDUCTOR = driver.CODIGO
    vehicle.ESTADO = '01'
    vehicle.FEC_ESTADO = data.delivery_date
    driver.UND_NRO = data.vehicle_number
    driver.CUO_DIARIA = vehicle.CUO_DIARIA

    db.commit()

    return JSONResponse(content={"message": "Vehicle delivered successfully"}, status_code=200)
  
  except Exception as e:
    db.rollback()
    return JSONResponse(content={"error": str(e)}, status_code=500)
  
  finally:
    db.close()