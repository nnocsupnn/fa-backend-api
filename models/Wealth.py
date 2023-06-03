from sqlalchemy import Column, Integer, DateTime, ForeignKey, Float, func
from sqlalchemy.orm import relationship, joinedload

from config.db import Base, SessionLocal, engine

class Wealth(Base):
    __tablename__ = "wealth"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('user.id'), unique=True)
    real_properties_value = Column(Float, index=True, default=0)
    personal_properties_value = Column(Float, index=True, default=0)
    liquid_investments_value = Column(Float(asdecimal=True), index=True, default=0)
    other_investment_value = Column(Float(asdecimal=True), index=True, nullable=True, default=0)
    
    projected_rate_personal_properties = Column(Float(asdecimal=True), index=True, default=0)
    projected_rate_real_properties = Column(Float(asdecimal=True), index=True, default=0)
    projected_rate_liquid_investment = Column(Float(asdecimal=True), index=True, default=0)
    projected_rate_other_investment = Column(Float(asdecimal=True), index=True, default=0)
    
    tax_rate = Column(Float(asdecimal=True), index=True, nullable=False, default=0)
    current_provision = Column(Float(asdecimal=True), index=True, nullable=True, default=0)
    created_date = Column(DateTime, default=func.now())
    updated_date = Column(DateTime, default=func.now(), onupdate=func.now())
    
    user = relationship("User", back_populates=__tablename__, lazy="select")