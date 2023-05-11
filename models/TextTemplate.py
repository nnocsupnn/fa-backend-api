from sqlalchemy import Column, Integer, String, DateTime, func

from components.db import Base, SessionLocal, engine

class TextTemplate(Base):
    __tablename__ = "text_template"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(30), index=True, unique=True)
    description = Column(String(50), index=True)
    category = Column(String(50), index=True, nullable=False)
    created_date = Column(DateTime, default=func.now())
    updated_date = Column(DateTime, default=func.now(), onupdate=func.now())
    
    @staticmethod
    def getTemplate(subj: str):
        db = SessionLocal()
        result = db.query(TextTemplate).get({ "code": subj })
        db.close()
        return result