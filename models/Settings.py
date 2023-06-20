from sqlalchemy import Column, Integer, Enum, DateTime, func, Float
from sqlalchemy.orm import validates
from config.db import Base, SessionLocal, engine
from config.functions import make_code_string

'''
Settings
'''
class Settings(Base):
    __tablename__ = "settings"

    id = Column(Integer, primary_key=True, index=True)
    inflation_rate = Column(Float, index=True)
    theme = Column(Enum("light", "dark"), default="light", index=True)
    created_date = Column(DateTime, default=func.now())
    updated_date = Column(DateTime, default=func.now(), onupdate=func.now())