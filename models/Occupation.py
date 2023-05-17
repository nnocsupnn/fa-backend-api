from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship, validates
from config.db import Base, SessionLocal, engine
from models.TextTemplate import TextTemplate

class Occupation(Base):
    __tablename__ = "occupation"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String(50), index=True)
    rank = Column(String(35), index=True)
    industry = Column(String(35), index=True)
    created_date = Column(DateTime, default=func.now())
    updated_date = Column(DateTime, default=func.now(), onupdate=func.now())
    users = relationship("User", back_populates="occupation")

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
        try:
            with SessionLocal() as db:
                tt = db.query(TextTemplate).filter(TextTemplate.code == code).count()
                db.close()
                if tt == 0:
                    raise Exception(f"{key}={code} is not registered in text_templates")
                else:
                    return code
        except Exception as e:
            raise e
    
    @validates('rank')
    def validate_rank(self, key, rank):
        return self.validator(key, rank)
    
    @validates('industry')
    def validate_industry(self, key, industry):
        return self.validator(key, industry)