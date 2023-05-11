from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, func
from sqlalchemy.orm import relationship

from components.db import Base, SessionLocal, engine

class DependencyProvision(Base):
    __tablename__ = "dependency_provision"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), index=True)
    amount = Column(Float, index=True)
    created_date = Column(DateTime, default=func.now())
    updated_date = Column(DateTime, default=func.now(), onupdate=func.now())
    
    user = relationship("User", back_populates=__tablename__, cascade="all", lazy="select")
