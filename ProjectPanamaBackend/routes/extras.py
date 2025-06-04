from fastapi import APIRouter
from controller.extras import get_current_time

extras_router = APIRouter()

@extras_router.get("/extras/time/", tags=["extras"])
async def get_time():
  return await get_current_time()