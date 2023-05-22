from sqlalchemy import Column, Integer, DateTime, ForeignKey, Float, func
from sqlalchemy.orm import relationship, joinedload

from config.db import Base, SessionLocal, engine

class Kapritso(Base):
    __tablename__ = "kapritso"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('user.id'), unique=True)
    factor = Column(Float, index=True, nullable=False)
    daily_cost = Column(Float, index=True, nullable=False)
    
    created_date = Column(DateTime, default=func.now())
    updated_date = Column(DateTime, default=func.now(), onupdate=func.now())
    
    user = relationship("User", back_populates=__tablename__, lazy="select")