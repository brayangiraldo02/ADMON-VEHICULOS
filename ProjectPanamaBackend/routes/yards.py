from fastapi import APIRouter
from controller.yards import yards, vehicle_yard

yards_router = APIRouter()

@yards_router.get("/yards/{company_code}", tags=["Yards"])
async def get_yards(company_code: str):
  return await yards(company_code)

@yards_router.get("/yards/{company_code}/vehicle/{vehicle_number}", tags=["Yards"])
async def get_vehicle_yard(company_code: str, vehicle_number: str):
  return await vehicle_yard(company_code, vehicle_number)