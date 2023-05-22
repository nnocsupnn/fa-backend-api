from models import IncomeProtection, UserDetail
from interfaces.json import ExpensePatchJson
from config.db import SessionLocal as Session
from sqlalchemy.exc import NoResultFound

class IncomeProtectionService:
    
    def incomeProtections(userId: int):
        result = None
        with Session() as db:
            result = db.query(IncomeProtection).filter(IncomeProtection.user_id == userId).all()
            db.close()
            
        return result