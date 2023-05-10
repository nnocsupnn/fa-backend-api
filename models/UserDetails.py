from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship

from components.db import Base, SessionLocal, engine

class UserDetails(Base):
    __tablename__ = "user_details"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship("User", back_populates=__tablename__)
    year_business = Column(Integer, index=True)
    retirement_age = Column(Integer, index=True)
    retirement_package = Column(Float(asdecimal=True), unique=True, index=True)
    life_expectancy = Column(Integer, index=True)