from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship

from components.db import Base, SessionLocal, engine

class TextTemplate(Base):
    __tablename__ = "text_template"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(30), index=True)
    description = Column(String(50), index=True)
    created_date = Column(DateTime, default=func.now())
    updated_date = Column(DateTime, default=func.now(), onupdate=func.now())