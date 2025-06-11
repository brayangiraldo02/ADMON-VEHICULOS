from fastapi import APIRouter
from schemas.operations import DeliveryVehicleDriver
from controller.operations import get_vehicle_operation, get_driver_operation, delivery_vehicle_driver

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