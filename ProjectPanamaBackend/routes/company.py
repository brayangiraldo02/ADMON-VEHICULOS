from fastapi import APIRouter, Response
from controller.company import get_info_companies

import os
import json

base_dir = os.path.dirname(os.path.dirname(__file__)) 
json_file_path_10 = os.path.join(base_dir, 'temp', '10company-info.json')
json_file_path_58 = os.path.join(base_dir, 'temp', '58company-info.json')
json_file_path_ADMIN = os.path.join(base_dir, 'temp', 'admin-company-info.json')

company_router = APIRouter()

@company_router.get('/info-company/{company_code}/', tags=["Company"])
async def get_info_company(company_code: str):
  return await get_info_companies(company_code)