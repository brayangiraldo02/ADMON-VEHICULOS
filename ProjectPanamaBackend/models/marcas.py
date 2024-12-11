from sqlalchemy import Column, DateTime, CHAR
from config.dbconnection import Base
from datetime import datetime
import pytz

panama_timezone = pytz.timezone('America/Panama')
now_in_panama = datetime.now(panama_timezone)
fecha = now_in_panama.strftime("%Y-%m-%d %H:%M:%S")

class Marcas(Base):
  __tablename__ = 'MARCAS'

  CODIGO = Column(CHAR(2), primary_key=True, nullable=False)
  NOMBRE = Column(CHAR(30), default="")
  FEC_CREADO = Column(DateTime, default=fecha)
