from config.dbconnection import Base
from sqlalchemy import Column, String, Numeric, DateTime

class Centrales(Base):
  __tablename__ = 'CENTRALES'
  CODIGO = Column(String(12), primary_key=True, nullable=False)
  EMPRESA = Column(String(2), nullable=False)
  NOMBRE = Column(String(50))
  NIT = Column(Numeric(12, 0))
  CONTROL = Column(String(2))
  RUC = Column(String(18))
  CIUDAD = Column(String(5))
  DIRECCION = Column(String(60))
  TELEFONO = Column(String(30))
  CELULAR = Column(String(30))
  CONSECUTIV = Column(String(6))
  LETRA = Column(String(3))
  REPRESENTA = Column(String(40))
  REPRES_CED = Column(String(12))
  REPRES_NAC = Column(String(15))
  FICHA = Column(String(8))
  DOCUMENTO = Column(String(8))
  CONTACTO = Column(String(40))
  CORREO = Column(String(40))
  FEC_CREADO = Column(DateTime)
  USU_CREADO = Column(String(12))
  USU_MODIFI = Column(String(12))