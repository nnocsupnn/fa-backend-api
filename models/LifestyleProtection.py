from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, func
from sqlalchemy.orm import relationship

from config.db import Base, SessionLocal, engine

class LifestyleProtection(Base):
    __tablename__ = "lifestyle_protection"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), index=True, unique=True)
    existing_provision = Column(Float, index=True, nullable=False)
    source_fund = Column(Float, index=True, nullable=False)
    gov_fund = Column(Float, index=True, nullable=False)
    other_fund = Column(Float, index=True, nullable=False)
    
    created_date = Column(DateTime, default=func.now())
    updated_date = Column(DateTime, default=func.now(), onupdate=func.now())
    
    user = relationship("User", back_populates=__tablename__, cascade="all", lazy="select")