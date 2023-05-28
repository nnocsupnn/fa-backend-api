from sqlalchemy import Column, Integer, String, ForeignKey, Enum, DateTime, Date, func
from sqlalchemy.orm import relationship as rel, joinedload
from models import DependencyDetail
from config.db import Base, SessionLocal, engine

class Dependencies(Base):
    __tablename__ = "dependencies"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), index=True)
    name = Column(String(50), index=True, unique=True)
    gender = Column(Enum("female", "male"), index=True)
    relationship = Column(Enum("son", "daughter", "mother", "father", "grand_mother", "grand_father", "sister", "brother", "wife"), index=True)
    date_of_birth = Column(Date(), index=True)
    dependency_detail_id = Column(Integer, ForeignKey("dependency_detail.id"), index=True, unique=True)
    created_date = Column(DateTime, default=func.now())
    updated_date = Column(DateTime, default=func.now(), onupdate=func.now())
    
    user = rel("User", back_populates=__tablename__, cascade="all", lazy="select")
    dependency_detail = rel("DependencyDetail", back_populates=__tablename__, lazy="joined")
    
    
    @staticmethod
    def getDependencies():
        db = SessionLocal()
        dependencies = db.query(Dependencies).all()
        db.close()
        return dependencies
    
    @staticmethod
    def getDependenciesByUserId(userId: int):
        db = SessionLocal()
        dependencies = db.query(Dependencies).where(Dependencies.user_id == userId).all()
        db.close()
        return dependencies
    
    @staticmethod
    def getDependencyJoined(id: int):
        db = SessionLocal()
        dependency = db.query(Dependencies).options(joinedload(DependencyDetail)).filter(Dependencies.id == id).first()
        db.close()
        return dependency
    
    @staticmethod
    def getDependency(id: int):
        db = SessionLocal()
        dependency = db.query(Dependencies).filter(Dependencies.id == id).first()
        db.close()
        return dependency