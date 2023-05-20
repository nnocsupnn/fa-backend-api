from models import Expenses, UserDetail
from interfaces.json.api_dtos import ExpensePatchJson
from config.db import SessionLocal as Session
from sqlalchemy.exc import NoResultFound

class ExpensesServices:
    def getExpenses(userId: int):
        result = None
        with Session() as db:
            userDetail = db.query(UserDetail).filter(UserDetail.id == userId).first()
            
            result = db.query(Expenses).filter(Expenses.user_detail_id == userDetail.id).all()
            
            if result == None:
                db.close()
                raise NoResultFound(f"No expense found.")
            
            db.close()
            
        return result
    
    def getExpense(expenseId: int):
        
        result = None
        with Session() as db:
            
            result = db.query(Expenses).filter(Expenses.id == expenseId).first()
            if result == None:
                db.close()
                raise NoResultFound(f"No expense found.")
            
            db.close()
            
        return result
    
    def updateExpense(expenseId: int, expense: ExpensePatchJson):
        result = None
        with Session() as db:
            expenseObj = db.query(Expenses).filter(Expenses.id == expenseId).first()
            for field_name, field_type in expense.__annotations__.items():
                if getattr(expense, field_name) != None:
                    setattr(expenseObj, field_name, getattr(expense, field_name))
                    
            db.commit()
            db.refresh(expenseObj)
            db.close()
            result = expenseObj
            
        return result
    
    def deleteExpense(expenseId: int):
        with Session() as db:
            db.query(Expenses).where(Expenses.id == expenseId).delete()
            
            db.commit()
            db.close()
            
        return True