from models import UserDetail
from json import loads
from fastapi.exceptions import FastAPIError

from interfaces.json.api_dtos import User as UserJson, UserDetail as UserDetailJson
from config.db import SessionLocal as Session

class UserDetailService:
    def getDetail(id: int):
        detail = UserDetail.getUserDetail(id)
        return detail
    
    def update(id: int, request: UserDetailJson):
        db = Session()
        detail = db.query(UserDetail).filter(UserDetail.user_id == id).first()
        
        if detail == None:
            raise Exception("Detail not exists.")
        
        for field_name, field_type in request.__annotations__.items():
            if getattr(request, field_name) != None:
                setattr(detail, field_name, getattr(request, field_name))
                
        db.commit()
        db.refresh(detail)
        db.close()
        
        return detail