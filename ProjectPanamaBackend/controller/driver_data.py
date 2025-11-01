from fastapi.responses import JSONResponse
from config.dbconnection import session
from fastapi.encoders import jsonable_encoder
from schemas.driver_data import DriverData
from models.conductores import Conductores
from utils.images import decode_image
import os
from dotenv import load_dotenv

load_dotenv()

driver_documents_path = os.getenv('DRIVER_DOCS_PATH')

async def upload_signature(data: DriverData):
  db = session()
  try:
    driver = db.query(Conductores).filter(Conductores.EMPRESA == data.company_code, Conductores.UND_NRO == data.vehicle_number).first()
    if not driver:
      return JSONResponse(content={"message": "Driver not found"}, status_code=404)
    
    base_path = os.path.join(driver_documents_path, data.company_code, driver.CODIGO)
    os.makedirs(base_path, exist_ok=True)

    final_signature_path = os.path.join(base_path, f"{data.vehicle_number}_{driver.CODIGO}_firma.png")

    if os.path.exists(final_signature_path):
      return JSONResponse(content={"message": "Signature already exists"}, status_code=400)

    image_data = decode_image(data.base64)
    
    with open(final_signature_path, "wb") as f:
      f.write(image_data)

    return JSONResponse(content={"message": "Signature uploaded successfully"}, status_code=200)
  except Exception as e:
    return JSONResponse(content={"message": str(e)}, status_code=500)
  finally:
    db.close()

#-----------------------------------------------------------------------------------------------

async def upload_picture(data: DriverData):
  db = session()
  try:
    driver = db.query(Conductores).filter(Conductores.EMPRESA == data.company_code, Conductores.UND_NRO == data.vehicle_number).first()
    if not driver:
      return JSONResponse(content={"message": "Driver not found"}, status_code=404)
    
    base_path = os.path.join(driver_documents_path, data.company_code, driver.CODIGO)
    os.makedirs(base_path, exist_ok=True)

    final_picture_path = os.path.join(base_path, f"{data.vehicle_number}_{driver.CODIGO}_foto.png")

    if os.path.exists(final_picture_path):
      return JSONResponse(content={"message": "Picture already exists"}, status_code=400)

    image_data = decode_image(data.base64)

    with open(final_picture_path, "wb") as f:
      f.write(image_data)

    return JSONResponse(content={"message": "Picture uploaded successfully"}, status_code=200)
  except Exception as e:
    return JSONResponse(content={"message": str(e)}, status_code=500)
