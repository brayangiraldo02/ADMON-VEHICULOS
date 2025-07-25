from fastapi import APIRouter
from schemas.operations import DeliveryVehicleDriver, BillInfo
from controller.operations import *

operations_router = APIRouter()

@operations_router.get("/operations/deliveryvehicledriver/vehicle/{vehicle_number}/", tags=["Operations"])
async def get_vehicle_operations(vehicle_number: str):
  return await get_vehicle_operation(vehicle_number)

@operations_router.get("/operations/deliveryvehicledriver/driver/{driver_number}/", tags=["Operations"])
async def get_driver_operations(driver_number: str):
  return await get_driver_operation(driver_number)

@operations_router.post("/operations/deliveryvehicledriver/", tags=["Operations"])
async def post_delivery_vehicle_driver(data: DeliveryVehicleDriver):
  return await delivery_vehicle_driver(data)

@operations_router.get("/operations/generate-contract/info/{vehicle_number}/", tags=["Operations"])
async def get_vehicle_delivery_info(vehicle_number: str):
  return await vehicle_delivery_info(vehicle_number)

@operations_router.get("/operations/generate-contract/pdf/{vehicle_number}/", tags=["Operations"])
async def get_generate_contract(vehicle_number: str):
  return await generate_contract(vehicle_number)

@operations_router.post("/operations/validation/", tags=["Operations"])
async def post_validation(data: BillValidation):
  return await validation(data)

@operations_router.post("/operations/new-bill/", tags=["Operations"])
async def post_new_bill(data: BillInfo):
  return await new_bill(data)