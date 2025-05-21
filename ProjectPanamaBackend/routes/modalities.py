from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from config.dbconnection import session
from models.modalidades import Modalidades
from fastapi.encoders import jsonable_encoder

modalities_router = APIRouter()

@modalities_router.get("/modalities/", tags=["Modalities"])
async def get_modalities():
  db = session()
  try:
    modalities = db.query(Modalidades.CODIGO, Modalidades.NOMBRE).all()
    modalities = [{'codigo': modalitie.CODIGO, 'nombre': modalitie.NOMBRE} for modalitie in modalities]
    return JSONResponse(content=jsonable_encoder(modalities), status_code=200)
  except Exception as e:
    return JSONResponse(content=jsonable_encoder({'error': str(e)}), status_code=500)
  finally:
    db.close()