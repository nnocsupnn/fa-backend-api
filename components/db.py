from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import sys, os

from components.functions import load_classes_from_folder

Base = declarative_base()

# MySQL database configuration
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root@127.0.0.1/financial_analysis"
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

from models.User import User
from models.UserDetails import UserDetails
from models.Occupation import Occupation
