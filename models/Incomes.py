from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, func
from sqlalchemy.orm import relationship

from config.db import Base, SessionLocal, engine

class Incomes(Base):
    __tablename__ = "incomes"

    id = Column(Integer, primary_key=True, index=True)
    user_detail_id = Column(Integer, ForeignKey("user_detail.id"), index=True)
    income_amount = Column(Float, index=True, nullable=False)
    description = Column(String(50), index=True)
    income_started_date = Column(DateTime, index=True)
    income_end_date = Column(DateTime, index=True, default=None)
    active = Column(Integer, index=True)
    created_date = Column(DateTime, default=func.now())
    updated_date = Column(DateTime, default=func.now(), onupdate=func.now())
    
    user_detail = relationship("UserDetail", back_populates=__tablename__, cascade="all", lazy="select")