from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from components.db import Base, SessionLocal, engine

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