from fastapi import APIRouter, Response
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from config.dbconnection import session
from models.infoempresas import InfoEmpresas

import os
import json

base_dir = os.path.dirname(os.path.dirname(__file__)) 
json_file_path_10 = os.path.join(base_dir, 'temp', '10company-info.json')
json_file_path_58 = os.path.join(base_dir, 'temp', '58company-info.json')
json_file_path_ADMIN = os.path.join(base_dir, 'temp', 'admin-company-info.json')

company_router = APIRouter()

@company_router.get('/info-company/{company_code}/', tags=["Company"])
async def get_info_company(company_code: str):
  db = session()
  try:
    company = db.query(InfoEmpresas.NOMBRE, InfoEmpresas.NIT, InfoEmpresas.DIRECCION, InfoEmpresas.CIUDAD, InfoEmpresas.TELEFONO, InfoEmpresas.CORREO, InfoEmpresas.LOGO) \
      .filter(InfoEmpresas.ID == company_code) \
      .first()
    
    if company:
      company_data = {
        "name": company.NOMBRE,
        "nit": company.NIT,
        "direction": company.DIRECCION,
        "city": company.CIUDAD,
        "phone": company.TELEFONO,
        "email": company.CORREO,
        "logo": company.LOGO
      }
      return JSONResponse(content=jsonable_encoder(company_data))
    
    return JSONResponse(
      status_code=404,
      content={"message": "Company not found"}
    )

  except FileNotFoundError:
    return JSONResponse(
      status_code=404,
      content={"message": "File not found"}
    )
  
  except Exception as e:
    return JSONResponse(
        status_code=500,
        content={"message": f"An unexpected error occurred: {str(e)}"}
    )
  
  finally:
    db.close()