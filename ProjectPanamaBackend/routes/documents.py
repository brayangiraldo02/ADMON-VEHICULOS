from fastapi import APIRouter
from controller.documents import vehicle_documents

documents_router = APIRouter()

@documents_router.get("/documents/vehicle-documents/{company_code}/{vehicle_number}/", tags=["Documents"])
async def get_vehicle_documents(company_code: str, vehicle_number: str):
  return await vehicle_documents(company_code, vehicle_number)