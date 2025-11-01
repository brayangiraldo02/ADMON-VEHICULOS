from fastapi.responses import JSONResponse
from config.dbconnection import session
from fastapi.encoders import jsonable_encoder
from schemas.driver_data import DriverData
from models.conductores import Conductores
from models.vehiculos import Vehiculos
from models.propietarios import Propietarios
from models.centrales import Centrales
from models.estados import Estados
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
  finally:
    db.close()

#-----------------------------------------------------------------------------------------------

async def vehicle_driver_data(company_code: str):
  db = session()
  try:
    vehicles = db.query(
      Vehiculos, Conductores, Propietarios, Centrales, Estados
      ).join(Conductores, (Conductores.CODIGO == Vehiculos.CONDUCTOR) & (Conductores.EMPRESA == Vehiculos.EMPRESA)
      ).join(Propietarios, (Propietarios.CODIGO == Vehiculos.PROPI_IDEN) & (Propietarios.EMPRESA == Vehiculos.EMPRESA)
      ).join(Centrales, (Centrales.CODIGO == Vehiculos.CENTRAL) & (Centrales.EMPRESA == Vehiculos.EMPRESA)
      ).join(Estados, (Estados.CODIGO == Vehiculos.ESTADO) & (Estados.EMPRESA == Vehiculos.EMPRESA)
      ).filter(Vehiculos.EMPRESA == company_code
      ).all()

    if not vehicles:
       return JSONResponse(content={"message": "No se encontraron vehículos para la empresa."}, status_code=404)
    
    info = []

    for vehicle, driver, owner, central, state in vehicles:
      signature_path = ''
      has_signature = 0

      picture_path = ''
      has_picture = 0

      signature = os.path.join(driver_documents_path, company_code, driver.CODIGO, f"{vehicle.NUMERO}_{driver.CODIGO}_firma.png")
      if os.path.exists(signature):
        signature_path = signature
        has_signature = 1

      picture = os.path.join(driver_documents_path, company_code, driver.CODIGO, f"{vehicle.NUMERO}_{driver.CODIGO}_foto.png")
      if os.path.exists(picture):
        picture_path = picture
        has_picture = 1

      info.append({
        'vehicle_number': vehicle.NUMERO,
        'model': vehicle.NOMMARCA,
        'plate': vehicle.PLACA,
        'quota': vehicle.NRO_CUPO,
        'central': central.NOMBRE,
        'owner_name': owner.NOMBRE,
        'nro_delivery': vehicle.NROENTREGA,
        'daily_quota': vehicle.CUO_DIARIA,
        'deposit_value': vehicle.VLR_DEPOSI,
        'state_name': state.NOMBRE,
        'has_quota': 'Con Cupo' if vehicle.CON_CUPO == '1' else '',
        'driver_code': vehicle.CONDUCTOR,
        'driver_name': driver.NOMBRE,
        'driver_id': driver.CEDULA,
        'driver_phone': driver.TELEFONO,
        'driver_address': driver.DIRECCION,
        'contract_date': vehicle.FEC_CONTRA.strftime('%d/%m/%Y') if vehicle.FEC_CONTRA and hasattr(vehicle.FEC_CONTRA, 'strftime') else None,
        'has_signature': has_signature,
        'url_signature': signature_path,
        'has_picture': has_picture,
        'url_picture': picture_path
      })

    return JSONResponse(content=jsonable_encoder(info), status_code=200)
  except Exception as e:
    return JSONResponse(content={"message": str(e)}, status_code=500)
  finally:
    db.close()