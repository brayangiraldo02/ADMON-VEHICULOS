from fastapi import APIRouter
from schemas.inspections import InspectionInfo
from controller.inspections import owners_data, vehicles_data, drivers_data, inspections_info

inspections_router = APIRouter()

@inspections_router.get("/inspections/owners_data/{company_code}", tags=["Inspections"])
async def get_owners_data(company_code: str):
  return await owners_data(company_code)

@inspections_router.get("/inspections/vehicles_data/{company_code}", tags=["Inspections"])
async def get_vehicles_data(company_code: str):
  return await vehicles_data(company_code)

@inspections_router.get("/inspections/drivers_data/{company_code}", tags=["Inspections"])
async def get_drivers_data(company_code: str):
  return await drivers_data(company_code)

@inspections_router.post("/inspections/inspections_info", tags=["Inspections"])
async def post_inspections_info(data: InspectionInfo):
  return await inspections_info(data)