from fastapi import APIRouter
from fastapi.responses import JSONResponse
from config.dbconnection import session
from models.conductores import Conductores
from fastapi.encoders import jsonable_encoder

drivers_router = APIRouter()

@drivers_router.get("/drivers", tags=["Drivers"])
async def get_drivers():
  db = session()
  try:
    drivers = db.query(Conductores.CODIGO, Conductores.UND_NRO, Conductores.NOMBRE, Conductores.CEDULA, Conductores.TELEFONO, Conductores.FEC_INGRES, Conductores.CUO_DIARIA, Conductores.NROENTREGA, Conductores.NROENTPAGO, Conductores.NROENTSDO).all()

    drivers_list = [
      {
        'codigo': driver.CODIGO,
        'unidad': driver.UND_NRO,
        'nombre': driver.NOMBRE,
        'cedula': driver.CEDULA,
        'telefono': driver.TELEFONO,
        'fecha_ingreso': driver.FEC_INGRES,
        'cuota_diaria': driver.CUO_DIARIA,
        'nro_entrega': driver.NROENTREGA,
        'nro_pago': driver.NROENTPAGO,
        'nro_saldo': driver.NROENTSDO
      }
      for driver in drivers
    ]
    return JSONResponse(content=jsonable_encoder(drivers_list))
  except Exception as e:
    return JSONResponse(content={"error": str(e)})
  finally:
    db.close()