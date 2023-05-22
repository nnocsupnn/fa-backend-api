from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, Date, func
from sqlalchemy.orm import relationship

from config.db import Base, SessionLocal, engine

class IncomeProtection(Base):
    __tablename__ = "income_protection"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), index=True, unique=True)
    # income_amount = Column(Float, index=True)
    # date_started = Column(Date(), index=True, nullable=True)
    created_date = Column(DateTime, default=func.now())
    updated_date = Column(DateTime, default=func.now(), onupdate=func.now())
    
    user = relationship("User", back_populates=__tablename__, cascade="all", lazy="select")
    income_protection_provision = relationship("IncomeProtectionProvision", back_populates=__tablename__, cascade="all", lazy="joined")