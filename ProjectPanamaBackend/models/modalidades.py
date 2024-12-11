from config.dbconnection import Base
from sqlalchemy import Column, String, Numeric, DateTime, CHAR, DECIMAL, Date, Boolean

class Modalidades(Base):
  __tablename__ = "MODALIDADES"

  CODIGO = Column(CHAR(2), primary_key=True)
  NOMBRE = Column(CHAR(40), default='')
  FEC_CREADO = Column(Date, default=None)