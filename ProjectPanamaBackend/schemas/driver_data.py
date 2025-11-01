from pydantic import BaseModel
from typing import Optional
from datetime import date

class DriverData(BaseModel):
  company_code: str
  vehicle_number: str
  base64: str