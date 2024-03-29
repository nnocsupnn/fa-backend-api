from sqlalchemy import Column, Integer, Enum, DateTime, func, Float, String
from sqlalchemy.orm import validates
from config.db import Base, SessionLocal, engine
from config.functions import make_code_string
from datetime import datetime, timedelta

'''
Settings
'''
class LoginSession(Base):
    __tablename__ = "login_session"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    token_expr = Column(Integer, default=func.now())
    access_token = Column(String(500))
    created_date = Column(DateTime, default=func.now())
    updated_date = Column(DateTime, default=func.now(), onupdate=func.now())
    
    def isTokenExpired(self):
        return datetime.fromtimestamp(self.token_expr) - datetime.now() < timedelta(0)