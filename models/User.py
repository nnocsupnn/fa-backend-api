from sqlalchemy import Column, Integer, String, Enum, Date, ForeignKey
from sqlalchemy.orm import relationship
from components.db import Base, SessionLocal, engine
from models.Occupation import Occupation

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(35), index=True)
    last_name = Column(String(35), index=True)
    middle_name = Column(String(35), index=True)
    email_address = Column(String(50), unique=True, index=True)
    active = Column(Integer, index=True)
    date_of_birth = Column(Date(), index=True)
    marital = Column(Enum("single", "married", "divorced", "separated", "widowed"), index=True)
    occupation_id = Column(Integer, ForeignKey('occupation.id'), index=True)
    occupation = relationship("Occupation", back_populates="users")

    user_details = relationship("UserDetails", back_populates=__tablename__, cascade="all, delete-orphan")

    @staticmethod
    def get_user(user_id: int):
        db = SessionLocal()
        user = db.query(User).filter(User.id == user_id).first()
        db.close()
        return user
    
    @staticmethod
    def get_user_details(user_id: int):
        db = SessionLocal()
        details = db.query(User).filter(User.id == user_id).first().user_details
        db.close()
        return details
    
    @staticmethod
    def updateUser(user_id: int, update: Occupation):
        db = SessionLocal()
        user = db.query(User).filter(User.id == user_id).first()
        user.occupation_id = update['occupation_id']
        db.commit()
        db.close()
        return user
