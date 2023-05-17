from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, Enum, func
from sqlalchemy.orm import relationship

from config.db import Base, SessionLocal, engine

class DependencyDetail(Base):
    __tablename__ = "dependency_detail"

    id = Column(Integer, primary_key=True, index=True)
    dependency_id = Column(Integer, ForeignKey("dependencies.id"), index=True)
    type = Column(String(50), index=True)
    target_years = Column(Integer, index=True)
    target_entry_age = Column(Integer, index=True)
    age_before_entry = Column(Integer, index=True)
    primary_lvl_annual = Column(Float, index=True, nullable=False)
    secondary_lvl_annual = Column(Float, index=True, nullable=False)
    tertiary_lvl_annual = Column(Float, index=True, nullable=False)
    tuition_fee_incr_perc = Column(Integer, index=True, nullable=False)
    created_date = Column(DateTime, default=func.now())
    updated_date = Column(DateTime, default=func.now(), onupdate=func.now())
    
    dependencies = relationship("Dependencies", back_populates=__tablename__, cascade="all", lazy="select")