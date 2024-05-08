from pydantic import BaseModel

class userLogin(BaseModel):
  nombre: str
  password: str