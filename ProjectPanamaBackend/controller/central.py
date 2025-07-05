from fastapi.responses import JSONResponse
from config.dbconnection import session
from models.centrales import Centrales
from fastapi.encoders import jsonable_encoder

async def get_centrals():
  db = session()
  try:
    central = db.query(Centrales.CODIGO, Centrales.NOMBRE).all()
    central = [{'codigo': central.CODIGO, 'nombre': central.NOMBRE} for central in central]
    return JSONResponse(content=jsonable_encoder(central))
  except Exception as e:
    return JSONResponse(content=jsonable_encoder({'error': str(e)}))
  finally:
    db.close()