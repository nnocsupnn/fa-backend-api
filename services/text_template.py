from models import TextTemplate as TT
from json import loads
from config.functions import make_code_string
from fastapi.exceptions import FastAPIError
import re

from interfaces.json.api_dtos import TextTemplate
from config.db import SessionLocal as Session

class TextTemplateService:
    def templates():
        return TT.getTemplates()
    

    def template(subj: str):
        return TT.getTemplate(subj=subj)
    
    def save(subj: TextTemplate):
        db = Session()
        
        tt = TT(
            description=subj.description,
            category=subj.category
        )
        
        db.add(tt)
        db.commit()
        
        tt.code = make_code_string(subj.description) + "_" + str(tt.id)
        
        db.commit()
        db.close()
        
    def delete(code: str):
        db = Session()
        
        try:
        
            result = db.query(TextTemplate).where(TextTemplate.code == code).delete()
            
            db.commit()
            db.close()
            return result
        except Exception as e:
            db.close()
            raise e
            