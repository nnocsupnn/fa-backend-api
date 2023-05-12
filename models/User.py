from sqlalchemy import Column, Integer, String, Enum, Date, ForeignKey
from sqlalchemy.orm import relationship, joinedload, validates
from components.db import Base, SessionLocal, engine
from models.Occupation import Occupation
import bcrypt

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(35), index=True, nullable=False)
    last_name = Column(String(35), index=True)
    middle_name = Column(String(35), index=True)
    email_address = Column(String(50), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    active = Column(Integer, index=True, default=0)
    date_of_birth = Column(Date(), index=True)
    marital = Column(Enum("single", "married", "divorced", "separated", "widowed"), index=True, nullable=False)
    occupation_id = Column(Integer, ForeignKey('occupation.id'), index=True, nullable=True)
    user_level = Column(Enum("admin", "user"), index=True, default="user")
    
    # Relationships
    occupation = relationship("Occupation", back_populates="users", lazy="joined")
    user_detail = relationship("UserDetail", back_populates=__tablename__, lazy="joined", uselist=False)
    dependencies = relationship("Dependencies", back_populates=__tablename__, cascade="all", lazy="joined")
    dependency_provision = relationship("DependencyProvision", back_populates=__tablename__, cascade="all", lazy="joined")
    income_protection = relationship("IncomeProtection", back_populates=__tablename__, cascade="all", lazy="joined")

    @staticmethod
    def get_user(user_id: int):
        db = SessionLocal()
        user = db.query(User).options(joinedload(User.user_detail)).options(joinedload(User.occupation)).options(joinedload(User.dependencies)).filter(User.id == user_id).first()
        db.close()
        return user
    
    @staticmethod
    def get_user_detail(user_id: int):
        db = SessionLocal()
        details = db.query(User).filter(User.id == user_id).first().user_detail
        db.close()
        return details
    
    @staticmethod
    def updateOccupation(user_id: int, update: Occupation):
        db = SessionLocal()
        user = db.query(User).filter(User.id == user_id).first()
        user.occupation_id = update['occupation_id']
        db.commit()
        db.close()
        return user
    
    @validates('password')
    def validate_password(self, key, password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))