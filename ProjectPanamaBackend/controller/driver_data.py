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
    Vehiculos.NUMERO,
    Vehiculos.NOMMARCA,
    Vehiculos.PLACA,
    Vehiculos.NRO_CUPO,
    Vehiculos.NROENTREGA,
    Vehiculos.CUO_DIARIA,
    Vehiculos.VLR_DEPOSI,
    Vehiculos.CON_CUPO,
    Vehiculos.CONDUCTOR,
    Vehiculos.FEC_CONTRA,
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
      ).filter(Vehiculos.EMPRESA == company_code
      ).all()

    if not vehicles:
       return JSONResponse(content={"message": "No se encontraron vehículos para la empresa."}, status_code=404)
    
    info = []

    for row in vehicles:
      signature_path = ''
      has_signature = 0

      picture_path = ''
      has_picture = 0

      signature = os.path.join(driver_documents_path, company_code, row.driver_code, f"{row.NUMERO}_{row.driver_code}_firma.png")
      if os.path.exists(signature):
        signature_path = signature
        has_signature = 1

      picture = os.path.join(driver_documents_path, company_code, row.driver_code, f"{row.NUMERO}_{row.driver_code}_foto.png")
      if os.path.exists(picture):
        picture_path = picture
        has_picture = 1

      info.append({
        'vehicle_number': row.NUMERO,
        'model': row.NOMMARCA,
        'plate': row.PLACA,
        'quota': row.NRO_CUPO,
        'central': row.central_name,
        'owner_name': row.owner_name,
        'nro_delivery': row.NROENTREGA,
        'daily_quota': row.CUO_DIARIA,
        'deposit_value': row.VLR_DEPOSI,
        'state_name': row.state_name,
        'has_quota': 'Con Cupo' if row.CON_CUPO == '1' else '',
        'driver_code': row.driver_code,
        'driver_name': row.driver_name,
        'driver_id': row.driver_id,
        'driver_phone': row.driver_phone,
        'driver_address': row.driver_address,
        'contract_date': row.FEC_CONTRA.strftime('%d/%m/%Y') if row.FEC_CONTRA and hasattr(row.FEC_CONTRA, 'strftime') else None,
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