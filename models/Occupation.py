from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship, validates
from config.db import Base, SessionLocal, engine
from models.TextTemplate import TextTemplate

class Occupation(Base):
    __tablename__ = "occupation"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String(50), index=True)
    user_id = Column(Integer, ForeignKey("user.id"), index=True, unique=True)
    rank = Column(String(35), index=True)
    industry = Column(String(35), index=True)
    created_date = Column(DateTime, default=func.now())
    updated_date = Column(DateTime, default=func.now(), onupdate=func.now())
    
    user = relationship("User", back_populates=__tablename__, cascade="all", lazy="select")

    @staticmethod
    def insert():
        with SessionLocal() as session:
            session.add(
                Occupation(
                    description = "IT HEAD",
                    rank = "IT_VP",
                    industry = "IT_IND"
                )
            )

            session.commit()
        return

    def validator(self, key, code):
        if code == None:
            return
        with SessionLocal() as db:
            tt = db.query(TextTemplate).filter(TextTemplate.code == code).count()
            db.close()
            if tt == 0:
                raise Exception(f"{key}={code} is not registered in text_templates")
            else:
                return code
    
    @validates('rank')
    def validate_rank(self, key, rank):
        return self.validator(key, rank)
    
    @validates('industry')
    def validate_industry(self, key, industry):
        return self.validator(key, industry)