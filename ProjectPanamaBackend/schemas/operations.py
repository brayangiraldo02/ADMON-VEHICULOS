from pydantic import BaseModel
from typing import Optional
from datetime import date

class DeliveryVehicleDriver(BaseModel):
  vehicle_number: str;
  driver_number: str;
  delivery_date: str;

class BillValidation(BaseModel):
  company_code: str
  vehicle_number: str
  bill_date: date

class BillInfo(BaseModel):
  company_code: str
  vehicle_number: str
  driver_number: str
  bill_date: date
  description: str
  user: Optional[str] = ''