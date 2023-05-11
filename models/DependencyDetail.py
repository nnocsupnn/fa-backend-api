from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, func
from sqlalchemy.orm import relationship

from components.db import Base, SessionLocal, engine

class DependencyDetail(Base):
    __tablename__ = "dependency_detail"

    id = Column(Integer, primary_key=True, index=True)
    dependency_id = Column(Integer, ForeignKey("dependencies.id"), index=True)
    type = Column(String(50), index=True)
    target_years = Column(Integer, index=True)
    target_entry_age = Column(Integer, index=True)
    age_before_entry = Column(Integer, index=True)
    amount = Column(Float, index=True)
    created_date = Column(DateTime, default=func.now())
    updated_date = Column(DateTime, default=func.now(), onupdate=func.now())
    
    dependencies = relationship("Dependencies", back_populates=__tablename__, cascade="all", lazy="select")