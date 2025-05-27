from fastapi import APIRouter
from controller.cities import get_city

cities_router = APIRouter()

@cities_router.get("/cities/", tags=["Cities"])
async def get_cities():
  return await get_city()