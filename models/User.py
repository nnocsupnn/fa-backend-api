from sqlalchemy import Column, Integer, String, Enum, Date, ForeignKey, Boolean, func, Float
from sqlalchemy.orm import relationship, joinedload, validates
from config.db import Base, SessionLocal, engine
from models.Occupation import Occupation
import bcrypt

class User(Base):
    PW_ENCODING = "utf-8"
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(35), index=True, nullable=False)
    last_name = Column(String(35), index=True)
    middle_name = Column(String(35), index=True)
    gender = Column(Enum("male", "female"), index=True, nullable=False)
    email_address = Column(String(50), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    active = Column(Boolean, index=True, default=False)
    date_of_birth = Column(Date(), index=True)
    marital = Column(Enum("single", "married", "divorced", "separated", "widowed"), index=True, nullable=False)
    occupation_id = Column(Integer, ForeignKey('occupation.id'), index=True, nullable=True)
    user_level = Column(Enum("admin", "user"), index=True, default="user", nullable=False)
    deletable = Column(Boolean, index=True, default=False, nullable=False)
    basic_salary = Column(Float(asdecimal=True), index=True, default=0)
    net_salary = Column(Float(asdecimal=True), index=True, default=0)
    
    # Relationships
    occupation = relationship("Occupation", back_populates="users", lazy="joined")
    user_detail = relationship("UserDetail", back_populates=__tablename__, lazy="joined", uselist=False)
    dependencies = relationship("Dependencies", back_populates=__tablename__, cascade="all", lazy="joined")
    income_protection = relationship("IncomeProtection", back_populates=__tablename__, cascade="all", lazy="joined", uselist=False)
    lifestyle_protection = relationship("LifestyleProtection", back_populates=__tablename__, cascade="all", lazy="joined", uselist=False)
    lifestyle_protection_investments = relationship("LifestyleProtectionInvestments", back_populates=__tablename__, cascade="all", lazy="joined")
    wealth = relationship("Wealth", back_populates=__tablename__, cascade="all", lazy="joined", uselist=False)
    kapritso = relationship("Kapritso", back_populates=__tablename__, cascade="all", lazy="joined", uselist=False)

    @staticmethod
    def get_user(user_id: int):
        db = SessionLocal()
        user = db.query(User).options(joinedload(User.user_detail)).options(joinedload(User.occupation)).options(joinedload(User.dependencies)).filter(User.id == user_id).first()
        db.close()
        return user
    
    @staticmethod
    def get_users():
        db = SessionLocal()
        users = db.query(User).all()
        db.close()
        return users
    
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
        return bcrypt.hashpw(password.encode(self.PW_ENCODING), bcrypt.gensalt())
    
    def check_password(self, password):
        return bcrypt.checkpw(password.encode(self.PW_ENCODING), self.password.encode(self.PW_ENCODING))