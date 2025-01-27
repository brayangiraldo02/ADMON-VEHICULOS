from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from datetime import datetime
import pytz

extras_router = APIRouter()

@extras_router.get("/extras/time", tags=["extras"])
async def get_time():
  time = datetime.now(pytz.timezone('America/Panama'))
  fecha = time.strftime("%Y-%m-%d")
  return JSONResponse(content=jsonable_encoder({"time": fecha}), status_code=200)