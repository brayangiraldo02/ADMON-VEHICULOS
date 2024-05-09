from pydantic import BaseModel

class userLogin(BaseModel):
  user: str
  password: str