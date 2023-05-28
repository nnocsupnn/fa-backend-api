from models import Wealth
from interfaces.json import WealthPatchJson
from config.db import SessionLocal as Session
from sqlalchemy.exc import NoResultFound

class WealthService:
    
    def getWealths(userId: int):
        result = None
        
        with Session() as db:
            result = db.query(Wealth).filter(Wealth.user_id == userId).first()
            
            db.close()
            
        return result
    
    def updateWealth(userId: int, wealth: WealthPatchJson):
        result = None
        with Session() as db:
            result = db.query(Wealth).filter(Wealth.user_id == userId).first()
            
            for field, value in vars(wealth).items():
                if hasattr(result, field) and value != None:
                    setattr(result, field, value)
                    
            db.commit()
            db.refresh(result)
            db.close()
            
        return result