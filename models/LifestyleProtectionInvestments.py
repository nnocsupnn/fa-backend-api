from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, func
from sqlalchemy.orm import relationship

from config.db import Base, SessionLocal, engine

class LifestyleProtectionInvestments(Base):
    __tablename__ = "lifestyle_protection_investments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), index=True)
    age = Column(Integer, index=True, nullable=False, unique=True) # unique per age
    annual_investment = Column(Float, index=True)
    created_date = Column(DateTime, default=func.now())
    updated_date = Column(DateTime, default=func.now(), onupdate=func.now())
    
    user = relationship("User", back_populates=__tablename__, cascade="all", lazy="select")