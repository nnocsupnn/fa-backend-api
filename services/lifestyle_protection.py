from models import LifestyleProtection, LifestyleProtectionInvestments
from interfaces.json import IncomePatchJson
from config.db import SessionLocal as Session
from sqlalchemy.exc import NoResultFound

class LifestyleProtectionService:
    
    def getProtections(userId: int):
        result = None
        with Session() as db:
            result = db.query(LifestyleProtection).filter(LifestyleProtection.user_id == userId).first()
            db.close()
            
        return result
    
    
    def update():
        pass