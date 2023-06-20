from sqlalchemy import Column, Integer, Text, DateTime, func, Float
from sqlalchemy.orm import validates
from config.db import Base, SessionLocal, engine
from config.functions import make_code_string
from datetime import datetime, timedelta

'''
Settings
'''
class BlockedSession(Base):
    __tablename__ = "blocked_session"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(Text, nullable=False)
    created_date = Column(DateTime, default=func.now())
    updated_date = Column(DateTime, default=func.now(), onupdate=func.now())
    
    def isTokenExpired(self):
        return datetime.fromtimestamp(self.token_expr) - datetime.now() < timedelta(0)