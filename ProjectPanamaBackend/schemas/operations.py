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

class ChangeYard(BaseModel):
  company_code: str
  vehicle_number: str
  yard_code: str
  description: str

class ChangeVehicleState(BaseModel):
  company_code: str
  vehicle_number: str
  state_code: str
  yard_code: Optional[str] = None
  change_reason: str

class VehicleMileage(BaseModel):
  company_code: str
  vehicle_number: str
  mileage: int

class LoanVehicle(BaseModel):
  company_code: str
  original_vehicle: str
  loan_vehicle: str
  reason: str