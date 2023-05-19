from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, Enum, func
from sqlalchemy.orm import relationship

from config.db import Base, SessionLocal, engine

class DependencyDetail(Base):
    __tablename__ = "dependency_detail"

    id = Column(Integer, primary_key=True, index=True)
    dependency_provision_id = Column(Integer, ForeignKey("dependency_provision.id"), index=True)
    # type = Column(String(50), index=True)
    # target_years = Column(Integer, index=True)
    target_entry_age = Column(Integer, index=True)
    age_before_entry = Column(Integer, index=True)
    primary_lvl_annual = Column(Float, index=True, nullable=False)
    secondary_lvl_annual = Column(Float, index=True, nullable=False)
    tertiary_lvl_annual = Column(Float, index=True, nullable=False)
    
    primary_lvl_years = Column(Integer, index=True)
    secondary_lvl_years = Column(Integer, index=True)
    tertiary_lvl_years = Column(Integer, index=True)
    
    tuition_fee_incr_perc = Column(Float, index=True, nullable=False)
    created_date = Column(DateTime, default=func.now())
    updated_date = Column(DateTime, default=func.now(), onupdate=func.now())
    
    dependencies = relationship("Dependencies", back_populates=__tablename__, cascade="all", lazy="select")
    dependency_provision = relationship("DependencyProvision", back_populates=__tablename__, lazy="joined")
    dependencies = relationship("Dependencies", back_populates=__tablename__, lazy="joined")
    
    @staticmethod
    def getDetail(id: int):
        db = SessionLocal()
        detail = db.query(DependencyDetail).filter(DependencyDetail.dependency_id == id).first()
        db.close()
        
        return detail