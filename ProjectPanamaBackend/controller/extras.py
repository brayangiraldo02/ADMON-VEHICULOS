from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from datetime import datetime
import pytz

async def get_current_time():
  time = datetime.now(pytz.timezone('America/Panama'))
  fecha = time.strftime("%Y-%m-%d")
  return JSONResponse(content=jsonable_encoder({"time": fecha}), status_code=200)