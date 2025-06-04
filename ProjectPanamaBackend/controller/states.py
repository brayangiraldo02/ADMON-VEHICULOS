from fastapi.responses import JSONResponse
from config.dbconnection import session
from models.estados import Estados
from fastapi.encoders import jsonable_encoder

async def get_owner():
  db = session()
  try:
    states = db.query(Estados.CODIGO, Estados.NOMBRE).all()
    states_list = [{'id': state.CODIGO, 'name': state.NOMBRE} for state in states]
    return JSONResponse(content=jsonable_encoder(states_list))
  except Exception as e:
    return JSONResponse(content={"error": str(e)})
  finally:
    db.close()