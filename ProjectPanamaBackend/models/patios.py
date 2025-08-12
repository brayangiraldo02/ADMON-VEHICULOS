from config.dbconnection import Base
from sqlalchemy import Column, CHAR, DateTime

class Patios(Base):
  __tablename__ = 'PATIOS'
  EMPRESA = Column(CHAR(2), nullable=False)
  CODIGO = Column(CHAR(2), primary_key=True, nullable=False)
  NOMBRE = Column(CHAR(40))
  CIUDAD = Column(CHAR(5))
  DIRECCION = Column(CHAR(60))
  ENCARGADO = Column(CHAR(40))
  TELEFONO = Column(CHAR(20))
  CELULAR = Column(CHAR(20))
  FEC_CREADO = Column(DateTime)