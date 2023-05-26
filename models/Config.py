from sqlalchemy import Column, Integer, DateTime, ForeignKey, Float, func
from sqlalchemy.orm import relationship, joinedload

from config.db import Base, SessionLocal, engine

class Config(Base):
    __tablename__ = "config"

    id = Column(Integer, primary_key=True, index=True)
    inflation_rate = Column(Float(asdecimal=True), index=True, default=0)
    deduction_from_family_home = Column(Float(asdecimal=True), index=True, default=0)
    other_deduction = Column(Float(asdecimal=True), index=True, default=0)
    created_date = Column(DateTime, default=func.now())
    updated_date = Column(DateTime, default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates=__tablename__, lazy="select")