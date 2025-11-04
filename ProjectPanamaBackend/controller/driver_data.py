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
    
    base_path = os.path.join(driver_documents_path, data.company_code, driver.CODIGO, "firmas")
    os.makedirs(base_path, exist_ok=True)

    existing_signatures = [f for f in os.listdir(base_path) if f.startswith(f"{data.vehicle_number}_{driver.CODIGO}_firma")]

    next_index = len(existing_signatures) + 1

    final_signature_path = os.path.join(base_path, f"{data.vehicle_number}_{driver.CODIGO}_firma_{next_index}.png")

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

    final_picture_path = os.path.join(base_path, f"{driver.CODIGO}_foto.png")

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

async def vehicle_driver_data(company_code: str, vehicle_number: str):
  db = session()
  try:
    vehicle = db.query(
    Vehiculos.NUMERO,
    Vehiculos.NOMMARCA,
    Vehiculos.PLACA,
    Vehiculos.NRO_CUPO,
    Vehiculos.NROENTREGA,
    Vehiculos.CUO_DIARIA,
    Vehiculos.VLR_DEPOSI,
    Vehiculos.CON_CUPO,
    Vehiculos.CONDUCTOR,
    Conductores.CODIGO.label('driver_code'),
    Conductores.NOMBRE.label('driver_name'),
    Conductores.CEDULA.label('driver_id'),
    Conductores.TELEFONO.label('driver_phone'),
    Conductores.DIRECCION.label('driver_address'),
    Propietarios.NOMBRE.label('owner_name'),
    Centrales.NOMBRE.label('central_name'),
    Estados.NOMBRE.label('state_name')
      ).join(Conductores, (Conductores.CODIGO == Vehiculos.CONDUCTOR) & (Conductores.EMPRESA == Vehiculos.EMPRESA)
      ).join(Propietarios, (Propietarios.CODIGO == Vehiculos.PROPI_IDEN) & (Propietarios.EMPRESA == Vehiculos.EMPRESA)
      ).join(Centrales, (Centrales.CODIGO == Vehiculos.CENTRAL) & (Centrales.EMPRESA == Vehiculos.EMPRESA)
      ).join(Estados, (Estados.CODIGO == Vehiculos.ESTADO) & (Estados.EMPRESA == Vehiculos.EMPRESA)
      ).filter(Vehiculos.EMPRESA == company_code, Vehiculos.NUMERO == vehicle_number
      ).first()
    
    if not vehicle:
       return JSONResponse(content={"message": "No se encontraron vehículos para la empresa."}, status_code=404)
    
    signature_path = ''
    has_signature = 0

    picture_path = ''
    has_picture = 0

    signature = os.path.join(driver_documents_path, company_code, vehicle.driver_code, f"{vehicle.NUMERO}_{vehicle.driver_code}_firma.png")
    if os.path.exists(signature):
      signature_path = signature
      has_signature = 1

    picture = os.path.join(driver_documents_path, company_code, vehicle.driver_code, f"{vehicle.NUMERO}_{vehicle.driver_code}_foto.png")
    if os.path.exists(picture):
      picture_path = picture
      has_picture = 1

    info = {
      'vehicle_number': vehicle.NUMERO,
      'model': vehicle.NOMMARCA,
      'plate': vehicle.PLACA,
      'quota': vehicle.NRO_CUPO,
      'central': vehicle.central_name,
      'owner_name': vehicle.owner_name,
      'nro_delivery': vehicle.NROENTREGA,
      'daily_quota': vehicle.CUO_DIARIA,
      'deposit_value': vehicle.VLR_DEPOSI,
      'state_name': vehicle.state_name,
      'has_quota': 'Con Cupo' if vehicle.CON_CUPO == '1' else '',
      'driver_code': vehicle.driver_code,
      'driver_name': vehicle.driver_name,
      'driver_id': vehicle.driver_id,
      'driver_phone': vehicle.driver_phone,
      'driver_address': vehicle.driver_address,
      'has_signature': has_signature,
      'url_signature': signature_path,
      'has_picture': has_picture,
      'url_picture': picture_path
    }

    return JSONResponse(content=jsonable_encoder(info), status_code=200)
  except Exception as e:
    return JSONResponse(content={"message": str(e)}, status_code=500)
  finally:
    db.close()