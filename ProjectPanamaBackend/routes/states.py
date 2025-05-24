from fastapi import APIRouter
from fastapi.responses import JSONResponse
from config.dbconnection import session
from models.estados import Estados
from fastapi.encoders import jsonable_encoder

states_router = APIRouter()

# PETICIÓN DE LISTA DE PROPIETARIOS A LA BASE DE DATOS 
# ---------------------------------------------------------------------------------------------------------------
@states_router.get("/states/", tags=["States"])
async def get_owners():
  db = session()
  try:
    states = db.query(Estados.CODIGO, Estados.NOMBRE).all()
    states_list = [{'id': state.CODIGO, 'name': state.NOMBRE} for state in states]
    return JSONResponse(content=jsonable_encoder(states_list))
  except Exception as e:
    return JSONResponse(content={"error": str(e)})
  finally:
    db.close()
# ---------------------------------------------------------------------------------------------------------------