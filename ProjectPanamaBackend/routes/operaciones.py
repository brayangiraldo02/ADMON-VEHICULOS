from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from config.dbconnection import session
from sqlalchemy.orm import aliased
from models.conductores import Conductores
from schemas.reports import *
from middlewares.JWTBearer import JWTBearer
from fastapi.encoders import jsonable_encoder
from utils.reports import *
from datetime import datetime
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
import jinja2
from utils.pdf import html2pdf


operations_router = APIRouter()

""" @operations_router.get("/operations/", tags=["Operations"])
async def verify_driver(driver_id: int):
  db = session()
  try:
        driver_condition = db.query(
            Conductores.CODIGO, Conductores.UND_NRO, Conductores.UND_PRE, Conductores.NOMBRE, Conductores.CEDULA,
            Conductores.TELEFONO, Conductores.FEC_INGRES, Conductores.CUO_DIARIA, Conductores.NROENTREGA,
            Conductores.NROENTPAGO, Conductores.NROENTSDO, Conductores.LICEN_VCE, Conductores.CONTACTO,
            Conductores.TEL_CONTAC, Conductores.PAR_CONTAC, Conductores.CONTACTO1, Conductores.TEL_CONTA1,
            Conductores.PAR_CONTA1
        ).filter(
            Conductores.CODIGO == driver_id
        ).first()
    
  if not driver_condition:
    return JSONResponse(content={"error": "Driver not found"})
  driver_conditions = {
        'codigo': driver_condition.CODIGO,
        'unidad': driver_condition.UND_NRO + ' - ' + driver_condition.UND_PRE,
        'nombre': driver_condition.NOMBRE,
        'cedula': driver_condition.CEDULA,
        'telefono': driver_condition.TELEFONO,
        'fecha_ingreso': driver_condition.FEC_INGRES,
        'cuota_diaria': driver_condition.CUO_DIARIA,
        'nro_entrega': driver_condition.NROENTREGA,
        'nro_pago': driver_condition.NROENTPAGO,
        'nro_saldo': driver_condition.NROENTSDO,
        'vce_licen': driver_condition.LICEN_VCE,
        'contacto': driver_condition.CONTACTO + ' - ' + driver_condition.TEL_CONTAC + ' - ' + driver_condition.PAR_CONTAC,
        'contacto1': driver_condition.CONTACTO1 + ' - ' + driver_condition.TEL_CONTA1 + ' - ' + driver_condition.PAR_CONTA1
  }
  return JSONResponse(content=jsonable_encoder(driver_conditions))
  except Exception as e:
    return JSONResponse(content={"error": str(e)})
  finally:
        db.close() """