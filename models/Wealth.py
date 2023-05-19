from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship, joinedload

from config.db import Base, SessionLocal, engine

class Wealth(Base):
    __tablename__ = "wealth"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    real_properties_value = Column(Float, index=True)
    personal_properties_value = Column(Float, index=True)
    liquid_investments_value = Column(Float(asdecimal=True), index=True)
    projected_apprec_rate_per_year = Column(Float(asdecimal=True), index=True)
    projected_rate_return_on_fixed = Column(Float(asdecimal=True), index=True)
    tax_rate = Column(Float(asdecimal=True), index=True, nullable=False)
    
    user = relationship("User", back_populates=__tablename__, lazy="select")