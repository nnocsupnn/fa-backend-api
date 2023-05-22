from models import IncomeProtection, IncomeProtectionProvision
from interfaces.json import IncomeProtectionPostJson, IncomeProtectionProvisionPostJson, IncomeProtectionProvisionPatchJson
from config.db import SessionLocal as Session
from sqlalchemy.exc import NoResultFound
from decimal import Decimal
from datetime import date, datetime
from sqlalchemy.orm import joinedload
class IncomeProtectionService:
    
    def incomeProtections(userId: int):
        result = None
        with Session() as db:
            result = db.query(IncomeProtection).filter(IncomeProtection.user_id == userId).first()
            db.close()
            
        return result
    
    def incomeProtection(incomeProtectionId: int):
        result = None
        with Session() as db:
            result = db.query(IncomeProtection).filter(IncomeProtection.id == incomeProtectionId).first()
            db.close()
            
        return result
    
    
    def saveIncomeProtection(incomeProtectionJson: IncomeProtectionPostJson, userId: int):
        result = None
        with Session() as db:
            incomeProtection = IncomeProtection(user_id=userId)
                
            db.add(incomeProtection)
            db.commit()
            
            
            db.commit()
            
            for field, value in vars(incomeProtectionJson).items():
                if type(value) in (int, float, str, bool, tuple, date, datetime, Decimal):
                    if hasattr(incomeProtection, field):
                        setattr(incomeProtection, field, value)
                elif isinstance(value, list):
                    for obj in value:
                        IncomeProtectionProvisionObj = IncomeProtectionProvision(income_protection_id=incomeProtection.id)
                        db.add(IncomeProtectionProvisionObj)
                        for subField, subValue in vars(obj).items():
                            if hasattr(IncomeProtectionProvisionObj, subField):
                                setattr(IncomeProtectionProvisionObj, subField, subValue)
            
            db.commit()
            result = db.query(IncomeProtection).filter(IncomeProtection.id == incomeProtection.id).first()
            db.close()
            
        return result
    
    def saveIncomeProtectionProvision(incomeProtectionProvisionPost: IncomeProtectionProvisionPostJson, incomeProtectionId: int):
        result = None
        with Session() as db:
            IncomeProtectionProvisionObj = IncomeProtectionProvision(income_protection_id=incomeProtectionId, amount=incomeProtectionProvisionPost.amount)
            db.add(IncomeProtectionProvisionObj)
            db.commit()
            db.close()
            
            result = db.query(IncomeProtection).filter(IncomeProtection.id == incomeProtectionId).first()
        return result
    
    def updateIncomeProtection(incomeProtectionId: int, incomeProtectionProvisionId: int, incomeProtectionJson: IncomeProtectionProvisionPatchJson):
        
        result = None
        with Session() as db:
            result = db.query(IncomeProtectionProvision)\
                .filter(
                    IncomeProtectionProvision.income_protection_id == incomeProtectionId,
                    IncomeProtectionProvision.id == incomeProtectionProvisionId
                ).first()
            
            for field, value in vars(incomeProtectionJson).items():
                if hasattr(result, field):
                    setattr(result, field, value)
                    
            db.commit()
            db.refresh(result)
            db.close()
            
        return result