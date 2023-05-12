from sqlalchemy import Column, Integer, String, ForeignKey, Enum, DateTime, Date, func
from sqlalchemy.orm import relationship as rel

from components.db import Base, SessionLocal, engine

class Dependencies(Base):
    __tablename__ = "dependencies"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), index=True)
    name = Column(String(50), index=True)
    gender = Column(Enum("female", "male"), index=True)
    relationship = Column(Enum("son", "daughter", "mother", "father", "grand_mother", "grand_father", "sister", "brother"), index=True)
    date_of_birth = Column(Date(), index=True)
    created_date = Column(DateTime, default=func.now())
    updated_date = Column(DateTime, default=func.now(), onupdate=func.now())
    
    user = rel("User", back_populates=__tablename__, cascade="all", lazy="select")
    dependency_detail = rel("DependencyDetail", back_populates=__tablename__, lazy="select", cascade="all")