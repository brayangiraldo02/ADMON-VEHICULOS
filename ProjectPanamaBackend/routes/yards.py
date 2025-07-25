from fastapi import APIRouter
from controller.yards import yards

yards_router = APIRouter()

@yards_router.get("/yards/{company_code}", tags=["Yards"])
async def get_yards(company_code: str):
  return await yards(company_code)