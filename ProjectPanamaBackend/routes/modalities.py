from fastapi import APIRouter, Depends
from controller.modalities import get_modality

modalities_router = APIRouter()

@modalities_router.get("/modalities/", tags=["Modalities"])
async def get_modalities():
  return await get_modality()