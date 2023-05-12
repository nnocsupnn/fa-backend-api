from models import User
from json import loads
from fastapi.exceptions import FastAPIError

from interfaces.json.api_dtos import User as UserJson
from components.db import SessionLocal as Session

class UserService:
    
    def getUser(id: int):
        try:
            user = User.get_user(id)
            if (user == None):
                raise Exception("User not found.")
            return user
        except Exception as e:
            raise e
    
    
    def user(user):
        try:
            # Process data below
            print(user)
            # with self.session() as session:
            #     session.add()
            # End Process
            
            return loads(user)
        except Exception as e:
            raise e
        
    def updateUser(id, user: UserJson):
        for field_name, field_type in user.__annotations__.items():
            print(getattr(user, field_name))
        
        return loads(user.json())