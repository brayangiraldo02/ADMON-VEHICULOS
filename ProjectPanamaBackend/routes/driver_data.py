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