from fastapi import APIRouter, UploadFile, File
from schemas.inspections import InspectionInfo
from controller.inspections import owners_data, vehicles_data, drivers_data, inspections_info, upload_image

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

@inspections_router.post("/inspections/inspections_info/{company_code}", tags=["Inspections"])
async def post_inspections_info(data: InspectionInfo, company_code: str):
  return await inspections_info(data, company_code)

@inspections_router.post("/inspections/upload_image/{vehicle_number}/", tags=["Inspections"])
async def post_upload_image(vehicle_number: str, file: UploadFile = File(...)):
    return await upload_image(vehicle_number, file)