from fastapi import APIRouter
from schemas.driver_data import DriverData
from controller.driver_data import *

driver_data_router = APIRouter()

@driver_data_router.post("/driver/upload-signature/", tags=["Driver Data"])
async def post_upload_signature(data: DriverData):
  return await upload_signature(data)

@driver_data_router.post("/driver/upload-picture/", tags=["Driver Data"])
async def post_upload_picture(data: DriverData):
  return await upload_picture(data)

@driver_data_router.post("/driver/upload-vehicle-photo/", tags=["Driver Data"])
async def post_upload_vehicle_photo(data: DriverData):
  return await upload_vehicle_photo(data)

@driver_data_router.get("/driver/vehicle-data/{company_code}/{vehicle_number}", tags=["Driver Data"])
async def get_vehicle_driver_data(company_code: str, vehicle_number: str):
  return await vehicle_driver_data(company_code, vehicle_number)