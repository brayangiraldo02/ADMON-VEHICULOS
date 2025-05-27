from fastapi.responses import JSONResponse
from config.dbconnection import session
from models.ciudades import Ciudades
from fastapi.encoders import jsonable_encoder

async def get_city():
  db = session()
  try:
    cities = db.query(Ciudades.CODIGO, Ciudades.NOMBRE).all()
    cities = [{'codigo': city.CODIGO, 'nombre': city.NOMBRE} for city in cities]
    return JSONResponse(content=jsonable_encoder(cities))
  except Exception as e:
    return JSONResponse(content=jsonable_encoder({'error': str(e)}))
  finally:
    db.close()