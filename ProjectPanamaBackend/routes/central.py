from fastapi import APIRouter
from controller.central import get_centrals

central_router = APIRouter()

@central_router.get("/central/", tags=["Central"])
async def get_central():
  return await get_centrals()