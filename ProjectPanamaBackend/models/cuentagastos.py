from config.dbconnection import Base
from sqlalchemy import Column, String, Numeric, DateTime, CHAR, DECIMAL, Date, Boolean

class CuentaGastos(Base):
  __tablename__ = "CUENTAGASTOS"

  CODIGO = Column(CHAR(12), primary_key=True)
  NOMBRE = Column(CHAR(50), default='')
  CTA_SINIE = Column(CHAR(12), default='')
  CTA_VENTAS = Column(CHAR(12), default='')
  FEC_CREADO = Column(Date, default=None)