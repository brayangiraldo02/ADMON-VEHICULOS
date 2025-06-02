from fastapi import APIRouter
from controller.states import get_owner

states_router = APIRouter()

# PETICIÓN DE LISTA DE PROPIETARIOS A LA BASE DE DATOS 
# ---------------------------------------------------------------------------------------------------------------
@states_router.get("/states/", tags=["States"])
async def get_owners():
  return await get_owner()
# ---------------------------------------------------------------------------------------------------------------