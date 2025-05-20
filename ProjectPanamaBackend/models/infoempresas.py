from sqlalchemy import Column, CHAR
from config.dbconnection import Base

class InfoEmpresas(Base):
  __tablename__ = 'INFOEMPRESAS'

  ID = Column(CHAR(2), primary_key=True)
  NOMBRE = Column(CHAR(100))
  NIT = Column(CHAR(100))
  DIRECCION = Column(CHAR(100))
  CIUDAD = Column(CHAR(100))
  TELEFONO = Column(CHAR(100))
  CORREO = Column(CHAR(100))
  LOGO = Column(CHAR(500))