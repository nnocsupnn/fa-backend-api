from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship, joinedload

from config.db import Base, SessionLocal, engine

class UserDetail(Base):
    __tablename__ = "user_detail"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    year_business = Column(Integer, index=True)
    retirement_age = Column(Integer, index=True)
    retirement_package = Column(Float(asdecimal=True), index=True)
    life_expectancy = Column(Integer, index=True)
    avg_annual_salary_incr = Column(Float(asdecimal=True), index=True, default=0)
    max_age_of_dependent = Column(Integer, index=True, default=0)
    min_age_of_dependent = Column(Integer, index=True, default=0)
    
    user = relationship("User", back_populates=__tablename__, lazy="select")
    incomes = relationship("Incomes", back_populates=__tablename__, lazy="joined")
    expenses = relationship("Expenses", back_populates=__tablename__, lazy="joined")
    
    def getUserDetail(id: int):
        db = SessionLocal()
        result = db.query(UserDetail)\
            .options(joinedload(UserDetail.incomes))\
            .options(joinedload(UserDetail.expenses))\
            .filter(UserDetail.user_id == id)\
            .first()
            
        db.close()
        return result