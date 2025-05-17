from fastapi import APIRouter, Response
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

import os
import json

base_dir = os.path.dirname(os.path.dirname(__file__)) 
json_file_path_10 = os.path.join(base_dir, 'temp', '10company-info.json')
json_file_path_58 = os.path.join(base_dir, 'temp', '58company-info.json')
json_file_path_ADMIN = os.path.join(base_dir, 'temp', 'admin-company-info.json')

company_router = APIRouter()

@company_router.get('/info-company/{company_code}', tags=["Company"])
async def get_info_company(company_code: str):
  try:
    if company_code == "10":
      company_data = json_file_path_10
    elif company_code == "58":
      company_data = json_file_path_58
    elif company_code == "A":
      company_data = json_file_path_ADMIN
    else:
      return JSONResponse(
        status_code=400, 
        content={"message": "Invalid company code"}
      )

    with open(company_data, 'r', encoding='utf-8') as file:
      data = json.load(file)
      json_data = jsonable_encoder(data)
      return JSONResponse(content=json_data)

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