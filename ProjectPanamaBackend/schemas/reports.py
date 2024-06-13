from pydantic import BaseModel
from typing import List

class userInfo(BaseModel):
  user: str

class infoReports(BaseModel):
  usuario: str
  empresas: List[str]
  estados: List[str]