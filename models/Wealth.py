from sqlalchemy import Column, Integer, DateTime, ForeignKey, Float, func
from sqlalchemy.orm import relationship, joinedload

from config.db import Base, SessionLocal, engine

class Wealth(Base):
    __tablename__ = "wealth"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('user.id'), unique=True)
    real_properties_value = Column(Float, index=True)
    personal_properties_value = Column(Float, index=True)
    liquid_investments_value = Column(Float(asdecimal=True), index=True)
    projected_apprec_rate_per_year = Column(Float(asdecimal=True), index=True)
    projected_rate_return_on_fixed = Column(Float(asdecimal=True), index=True)
    tax_rate = Column(Float(asdecimal=True), index=True, nullable=False)
    
    created_date = Column(DateTime, default=func.now())
    updated_date = Column(DateTime, default=func.now(), onupdate=func.now())
    
    user = relationship("User", back_populates=__tablename__, lazy="select")