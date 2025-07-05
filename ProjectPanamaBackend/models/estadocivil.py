from config.dbconnection import Base
from sqlalchemy import Column, CHAR, Numeric, DateTime

class EstadoCivil(Base):
  __tablename__ = 'ESTADOCIVIL'
  EMPRESA = Column(CHAR(2), nullable=False)
  CODIGO = Column(CHAR(1), primary_key=True, nullable=False)
  NOMBRE = Column(CHAR(15))
  FEC_CREADO = Column(DateTime)