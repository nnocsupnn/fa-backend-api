from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, func
from sqlalchemy.orm import relationship

from components.db import Base, SessionLocal, engine

class Expenses(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    user_detail_id = Column(Integer, ForeignKey("user_details.id"), index=True)
    expense_amount = Column(Float, index=True)
    expense_type = Column(String(30), index=True)
    description = Column(String(50), index=True)
    expense_started_date = Column(DateTime, index=True)
    expense_end_date = Column(DateTime, index=True)
    active = Column(Integer, index=True)
    created_date = Column(DateTime, default=func.now())
    updated_date = Column(DateTime, default=func.now(), onupdate=func.now())
    
    user_details = relationship("UserDetails", back_populates=__tablename__, cascade="all", lazy="select")