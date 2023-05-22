from models import LifestyleProtection, LifestyleProtectionInvestments
from interfaces.json import IncomePatchJson
from config.db import SessionLocal as Session
from sqlalchemy.exc import NoResultFound

class WealthService:
    
    def getProtections(userId: int):
        pass