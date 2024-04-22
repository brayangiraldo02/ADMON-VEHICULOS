from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Database connection
DATABASE_URL = "mysql+pymysql://softwar1_wp:=gp3w]#A[o1n@host45.latinoamericahosting.com:3306/softwar1_AdmonVehiculos"

# database motor
engine = create_engine(DATABASE_URL)

# Session generator
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declarative base class
Base = declarative_base()