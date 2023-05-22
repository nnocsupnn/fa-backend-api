from models import Kapritso
from interfaces.json import KapritsoPatchJson
from config.db import SessionLocal as Session
from sqlalchemy.exc import NoResultFound

class KapritsoService:
    
    def getKapritso(userId: int):
        result = None
        
        with Session() as db:
            result = db.query(Kapritso).filter(Kapritso.user_id == userId).first()
            
            db.close()
            
        return result
    
    def updateKapritso(userId: int, kapritso: KapritsoPatchJson):
        result = None
        with Session() as db:
            result = db.query(Kapritso).filter(Kapritso.user_id == userId).first()
            
            for field, value in vars(kapritso).items():
                if hasattr(result, field) and value != None:
                    setattr(result, field, value)
                    
            db.commit()
            db.refresh(result)
            db.close()
            
        return result