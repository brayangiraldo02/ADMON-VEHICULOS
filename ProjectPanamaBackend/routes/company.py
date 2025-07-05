from fastapi import APIRouter, Response
from controller.company import get_info_companies

company_router = APIRouter()

@company_router.get('/info-company/{company_code}/', tags=["Company"])
async def get_info_company(company_code: str):
  return await get_info_companies(company_code)