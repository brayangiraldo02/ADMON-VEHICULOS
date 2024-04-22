from config.dbconnection import Base
from sqlalchemy import Column, String, Numeric, DateTime

class Estados(Base):
  __tablename__ = 'ESTADOS'
  CODIGO = Column(String(2), primary_key=True, nullable=False)
  ABREVIADO = Column(String(8))
  NOMBRE = Column(String(30))
  ESTADO = Column(Numeric(1, 0))
  SUMAR = Column(Numeric(1, 0))
  REPORTAR = Column(Numeric(1, 0))
  COBRARADM = Column(Numeric(1, 0))
  COLUMNA = Column(String(1))
  FEC_CREADO = Column(DateTime)
  EMPRESA = Column(String(2))