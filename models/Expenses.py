from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, func
from sqlalchemy.orm import relationship, validates
from models import TextTemplate
from config.db import Base, SessionLocal, engine
from sqlalchemy.exc import NoResultFound

class Expenses(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    user_detail_id = Column(Integer, ForeignKey("user_detail.id"), index=True)
    expense_amount = Column(Float, index=True, nullable=False)
    expense_category = Column(String(30), index=True, nullable=False)
    description = Column(String(50), index=True)
    expense_started_date = Column(DateTime, index=True)
    expense_end_date = Column(DateTime, index=True)
    active = Column(Integer, index=True)
    created_date = Column(DateTime, default=func.now())
    updated_date = Column(DateTime, default=func.now(), onupdate=func.now())
    
    user_detail = relationship("UserDetail", back_populates=__tablename__, cascade="all", lazy="select")
    
    def validator(self, key, code):
        with SessionLocal() as db:
            tt = db.query(TextTemplate).filter(TextTemplate.code == code).count()
            db.close()
            if tt == 0:
                raise NoResultFound(f"{key}={code} is not registered in text_templates")
            else:
                return code
    
    @validates('expense_category')
    def validate_rank(self, key, expense_category):
        return self.validator(key, expense_category)