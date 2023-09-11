from models import Incomes, UserDetail
from interfaces.json import IncomePatchJson, IncomePostJson
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
    
    def saveIncome(userId: int, income: IncomePostJson):
        result = None
        with Session() as db:
            userDetail = db.query(UserDetail).filter(UserDetail.user_id == userId).first()
            result = Incomes(
                user_detail_id=userDetail.id,
                income_amount=income.income_amount,
                description=income.description,
                income_started_date=income.income_started_date if income.income_started_date != None else None,
                income_end_date=income.income_end_date if income.income_end_date != None else None,
                active=income.active if income.active != None else 0,
            )
            
            db.add(result)
            db.commit()
            db.refresh(result)
            db.close()
            
        return result
    
    def deleteIncome(incomeId: int):
        with Session() as db:
            db.query(Incomes).where(Incomes.id == incomeId).delete()
            
            db.commit()
            db.close()
            
        return True