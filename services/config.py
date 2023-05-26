from models import Config
from interfaces.json import WealthPatchJson
from config.db import SessionLocal as Session
from sqlalchemy.exc import NoResultFound

class ConfigService:
    
    def getConfig(userId: int):
        pass