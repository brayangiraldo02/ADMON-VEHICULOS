from pydantic import BaseModel
from typing import Optional

class DeliveryVehicleDriver(BaseModel):
  vehicle_number: str;
  driver_number: str;
  delivery_date: str;