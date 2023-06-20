from models import Config
from interfaces.json import ConfigPatchJson
from config.db import SessionLocal as Session
from sqlalchemy.exc import NoResultFound

class ConfigService:
    
    def initializeConfig():
        with Session() as db:
            isConfigExist = db.query(Config).count()
            if isConfigExist == 0:
                config = Config(
                    inflation_rate=0,
                    deduction_from_family_home=10000000,
                    other_deduction=5000000
                )
                
                db.add(config)
                db.commit()
            db.close()
            
    def getConfig():
        result = None
        with Session() as db:
            result = db.query(Config).first()
            db.close()
            
        return result
    
    def updateConfig(config: ConfigPatchJson):
        result = None
        with Session() as db:
            result = db.query(Config).first()
            for field, val in config.__annotations__.items():
                if hasattr(result, field) != None:
                    setattr(result, field, getattr(config, field))
                    
            
            db.commit()
            db.refresh(result)
            db.close()
            
        return result