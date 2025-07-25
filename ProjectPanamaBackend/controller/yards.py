from fastapi.responses import JSONResponse
from config.dbconnection import session
from models.patios import Patios
from fastapi.encoders import jsonable_encoder

async def yards(company_code: str):
  db = session()
  try:
    yards_info = db.query(Patios.CODIGO, Patios.NOMBRE).filter(Patios.EMPRESA == company_code).all()

    if not yards_info:
      return JSONResponse(content={"message": "No hay patios"}, status_code=404)

    yards_list = [{'id': yard.CODIGO, 'name': yard.NOMBRE} for yard in yards_info]
    return JSONResponse(content=jsonable_encoder(yards_list))
  except Exception as e:
    return JSONResponse(content={"message": str(e)}, status_code=500)
  finally:
    db.close()