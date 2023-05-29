from models import LifestyleProtection, LifestyleProtectionInvestments
from interfaces.json import LifestyleProtectionPatchJson, LifestyleProtectionInvestmentsPostJson, LifestyleProtectionInvestmentsPatchJson
from config.db import SessionLocal as Session
from sqlalchemy.exc import NoResultFound

class LifestyleProtectionService:
    
    def getProtections(userId: int):
        result = None
        with Session() as db:
            result = db.query(LifestyleProtection).filter(LifestyleProtection.user_id == userId).first()
            db.close()
            
        return result
    
    
    def update(userId: int, lifestyleProtection: LifestyleProtectionPatchJson):
        result = None
        
        with Session() as db:
            result = db.query(LifestyleProtection).filter(LifestyleProtection.user_id == userId).first()
            
            for field, value in vars(lifestyleProtection).items():
                if hasattr(result, field) and value != None:
                    setattr(result, field, value)
                    
                    
            db.commit()
            db.refresh(result)
            db.close()
            
        return result
    
    def getInvestmentsById(investmentId: int):
        result = None
        with Session() as db:
            result = db.query(LifestyleProtectionInvestments).filter(LifestyleProtectionInvestments.id == investmentId).first()
            
            db.close()
        
        return result
    
    def getInvestments(userId: int):
        result = None
        with Session() as db:
            result = db.query(LifestyleProtectionInvestments).filter(LifestyleProtectionInvestments.user_id == userId).all()
            
            db.close()
        
        return result
    
    def saveInvestment(userId: int, investment: LifestyleProtectionInvestmentsPostJson):
        result = None
        
        with Session() as db:
            invstmnt = LifestyleProtectionInvestments(user_id=userId)
            db.add(invstmnt)
            
            for field, value in vars(investment).items():
                if hasattr(invstmnt, field) and value != None:
                    setattr(invstmnt, field, value)
                    
                    
            db.commit()
            db.refresh(invstmnt)
            db.close()
            
            result = invstmnt
            
        return result
    
    def updateInvestment(userId: int, investment: LifestyleProtectionInvestmentsPatchJson):
        result = None
        
        with Session() as db:
            invstmnt = db.query(LifestyleProtectionInvestments).filter(LifestyleProtectionInvestments.user_id == userId, LifestyleProtectionInvestments.age == investment.age).first()
            
            if invstmnt == None:
                model = LifestyleProtectionInvestments(user_id=userId, age=investment.age, annual_investment=investment.annual_investment)
                db.add(model)
                db.commit()
                invstmnt = db.query(LifestyleProtectionInvestments).filter(LifestyleProtectionInvestments.id == model.id).first()
                
                
            for field, value in vars(investment).items():
                if hasattr(invstmnt, field) and value != None and field != "age":
                    setattr(invstmnt, field, value)
                    
                    
            db.commit()
            db.refresh(invstmnt)
            db.close()
            
            result = invstmnt
            
        return result