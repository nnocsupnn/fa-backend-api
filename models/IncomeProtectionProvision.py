from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, Date, func
from sqlalchemy.orm import relationship

from config.db import Base, SessionLocal, engine

class IncomeProtectionProvision(Base):
    __tablename__ = "income_protection_provision"

    id = Column(Integer, primary_key=True, index=True)
    income_protection_id = Column(Integer, ForeignKey("income_protection.id"), index=True)
    amount = Column(Float, index=True)
    created_date = Column(DateTime, default=func.now())
    updated_date = Column(DateTime, default=func.now(), onupdate=func.now())
    
    income_protection = relationship("IncomeProtection", back_populates=__tablename__, cascade="all", lazy="select")