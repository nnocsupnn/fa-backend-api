from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Config
from dotenv import dotenv_values
config = dotenv_values(".env")

Base = declarative_base()

# Config
DB_HOST = config['DB_HOST']
DB_USER = config['DB_USER']
DB_PW = config['DB_PW']
DB_NAME = config['DB_NAME']

# MySQL database configuration
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PW}@{DB_HOST}/{DB_NAME}"
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=False, pool_recycle=3600)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Importing the class is important to be able to read by the DB
from models import *
