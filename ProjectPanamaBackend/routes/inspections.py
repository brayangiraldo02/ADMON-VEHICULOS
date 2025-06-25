from fastapi import APIRouter
from controller.inspections import owners_data, vehicles_data, drivers_data
inspections_router = APIRouter()

@inspections_router.get("/owners_data/{company_code}", tags=["Inspections"])
async def get_owners_data(company_code: str):
  return await owners_data(company_code)

@inspections_router.get("/vehicles_data/{company_code}", tags=["Inspections"])
async def get_vehicles_data(company_code: str):
  return await vehicles_data(company_code)

@inspections_router.get("/drivers_data/{company_code}", tags=["Inspections"])
async def get_drivers_data(company_code: str):
  return await drivers_data(company_code)