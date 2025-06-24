from fastapi import APIRouter
from controller.inspections import owners_data
inspections_router = APIRouter()

@inspections_router.get("/owners_data/{company_code}", tags=["Inspections"])
async def get_owners_data(company_code: str):
  return await owners_data(company_code)