import json
from sqlalchemy.exc import IntegrityError
from fastapi import APIRouter, Response, status, Depends
from fastapi.exceptions import FastAPIError
from fastapi.responses import JSONResponse
from models import User
from sqlalchemy.orm import joinedload
from interfaces.route_interface import RouteInterface
from interfaces.json.api_dtos import User as UserJson, UserRegister
from services import UserService
from config.functions import serialize_model
from fastapi_jwt_auth import AuthJWT
import jwt
'''
UserAPI is class for User Resource

@interface RouteInterface
@author Nino Casupanan
@memberof MediCard
'''
class UserAPI(RouteInterface):
    def __init__(self, session):
        super().__init__()
        self.session = session
        self.router = APIRouter()
        self.setup_routes()
        
        # Services
        self.service = UserService
    
    def setup_routes(self):
        # Route Methodss
        @self.router.patch("/user/me", summary="Update current user")
        async def updateUser(request: UserJson, response: Response, auth: AuthJWT = Depends()):
            userId = auth.get_jwt_subject()
            print(userId)
            user = self.service.updateUser(userId, request)
            response.status_code = status.HTTP_200_OK
            return user
        
        @self.router.get("/user/me", summary="Get current user")
        async def me(auth: AuthJWT = Depends()):
            userId = auth.get_jwt_subject()
            user = User.get_user(user_id=userId)
            
            return user
        
        @self.router.get("/users", summary="Get all users", description="Note: this route is for `admin` role user.")
        async def getUsers(auth: AuthJWT = Depends()):
            userId = auth.get_jwt_subject()
            user = User.get_user(user_id=userId)
            
            if not user.user_level.__eq__("admin"):
                raise Exception("You are not allowed on this path.")
            
            users = User.get_users()
            return users
        
        
        @self.router.get("/user/{id}", summary="Get user", description="Note: this route is for `admin` role user.")
        async def getUser(id: int, response: Response) -> JSONResponse:
            user = self.service.getUser(id)
               
            if not user.user_level.__eq__("admin"):
                raise Exception("You are not allowed on this path.")
            
            response.status_code = status.HTTP_200_OK
            '''
            Get user
            '''
            return user
                
        @self.router.post("/user", status_code=status.HTTP_201_CREATED, summary="Register user")
        async def AddUser(request: UserRegister, response: Response):
            try:
                self.service.user(request)
                response.status_code = status.HTTP_201_CREATED
                return JSONResponse(
                    status_code=status.HTTP_201_CREATED,
                    content={
                        "status": status.HTTP_201_CREATED,
                        "message": "Your account is created. Please contact admin for activation."
                    }
                )
            except IntegrityError as e:
                return JSONResponse(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    content=self.default_error_response(str(e.__cause__))
                )
                
        @self.router.patch("/user/{id}", summary="Update user")
        async def updateUser(id: int, request: UserJson, response: Response):
            user = self.service.updateUser(id, request)
            response.status_code = status.HTTP_200_OK
            return user
            
        @self.router.delete("/user/{id}", summary="Delete user", status_code=status.HTTP_204_NO_CONTENT)
        async def deleteUser(id: int, response: Response):
            user = self.service.deleteUser(id)
            response.status_code = status.HTTP_204_NO_CONTENT
            return user