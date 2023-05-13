from models import UserDetail
from json import loads
from fastapi.exceptions import FastAPIError

from interfaces.json.api_dtos import User as UserJson
from components.db import SessionLocal as Session

class UserDetailService:
    def getDetail(id: int):
        detail = UserDetail.getUserDetail(id)
        print(detail)
        return detail