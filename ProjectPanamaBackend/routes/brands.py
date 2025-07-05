from fastapi import APIRouter
from controller.brands import get_brand

brands_router = APIRouter()

@brands_router.get("/brands/", tags=["Brands"])
async def get_brands():
    return await get_brand()