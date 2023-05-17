from models import User, Dependencies
from json import loads
from fastapi.exceptions import FastAPIError

from interfaces.json.api_dtos import User as UserJson, UserRegister
from config.db import SessionLocal as Session

class DependencyService:
    
    def dependency(id: int):
        db = Session()
        dependencies = db.query(Dependencies).where(Dependencies.user_id == id).all()
        
        return dependencies
        pass