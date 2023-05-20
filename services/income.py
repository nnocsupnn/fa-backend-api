from models import Incomes, UserDetail
from interfaces.json.api_dtos import IncomePatchJson
from config.db import SessionLocal as Session
from sqlalchemy.exc import NoResultFound

class IncomeService:
    
    def getIncomes(userId: int):
        
        result = None
        with Session() as db:
            userDetail = db.query(UserDetail).filter(UserDetail.id == userId).first()
            
            result = db.query(Incomes).filter(Incomes.user_detail_id == userDetail.id).all()
            if result == None:
                db.close()
                raise NoResultFound(f"No incomes found.")
            
            db.close()
            
        return result
    

    def getIncome(incomeId: int):
        
        result = None
        with Session() as db:
            
            result = db.query(Incomes).filter(Incomes.id == incomeId).first()
            
            if result == None:
                db.close()
                raise NoResultFound(f"No income found.")
            
            db.close()
            
        return result
    
    
    def updateIncome(incomeId: int, income: IncomePatchJson):
        result = None
        with Session() as db:
            incomeObj = db.query(Incomes).filter(Incomes.id == incomeId).first()
            if incomeObj == None:
                db.close()
                raise NoResultFound(f"No income found.")
            
            for field_name, field_type in income.__annotations__.items():
                if getattr(income, field_name) != None:
                    setattr(incomeObj, field_name, getattr(income, field_name))
                    
            db.commit()
            db.refresh(incomeObj)
            db.close()
            result = incomeObj
            
        return result
    
    def deleteIncome(incomeId: int):
        with Session() as db:
            db.query(Incomes).where(Incomes.id == incomeId).delete()
            
            db.commit()
            db.close()
            
        return True