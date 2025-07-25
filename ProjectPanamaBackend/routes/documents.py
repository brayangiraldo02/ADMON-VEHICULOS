from fastapi import APIRouter
from controller.documents import vehicle_documents, send_vehicle_documents, vehicle_info

documents_router = APIRouter()

@documents_router.get("/documents/vehicle-documents/{company_code}/{vehicle_number}/", tags=["Documents"])
async def get_vehicle_documents(company_code: str, vehicle_number: str):
  return await vehicle_documents(company_code, vehicle_number)

@documents_router.get("/documents/send-vehicle-documents/{company_code}/{vehicle_number}/{base_doc}/", tags=["Documents"])
async def get_send_vehicle_documents(company_code: str, vehicle_number: str, base_doc: str):
  return await send_vehicle_documents(company_code, vehicle_number, base_doc)

@documents_router.get("/documents/vehicle-info/{vehicle_number}/", tags=["Documents"])
async def get_vehicle_info(vehicle_number: str):
  return await vehicle_info(vehicle_number)