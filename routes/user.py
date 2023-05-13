import json
from fastapi import APIRouter, Response, status, Depends
from fastapi.exceptions import FastAPIError
from fastapi.responses import JSONResponse
from models import User
from sqlalchemy.orm import joinedload
from interfaces.route_interface import RouteInterface
from interfaces.json.api_dtos import User as UserJson, Occupation
from services import UserService
from decorator.json_encoder import CustomJSONEncoder
from components.functions import serialize_model
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
        
        @self.router.get("/user/me")
        async def me(auth: AuthJWT = Depends()):
            userId = auth.get_jwt_subject()
            user = User.get_user(user_id=userId)
            
            return user
        
        @self.router.get("/user/{id}")
        async def getUser(id: int, response: Response) -> JSONResponse:
            try:
                user = self.service.getUser(id)
               
                response.status_code = status.HTTP_200_OK
                return user
            except Exception as e:
                return JSONResponse(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    content=self.default_error_response(str(e))
                )
                
        @self.router.post("/user", status_code=status.HTTP_201_CREATED)
        async def user(request: UserJson, response: Response):
            try:
                user = request.json()
                self.service.user(user)
                return JSONResponse(
                    status_code=status.HTTP_201_CREATED,
                    content=json.loads(user)
                )
            except Exception as e:
                return JSONResponse(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    content=self.default_error_response(str(e))
                )
                
        @self.router.patch("/user/{id}", status_code=status.HTTP_201_CREATED)
        async def user(id: int, request: UserJson, response: Response):
            try:
                user = self.service.updateUser(id, request)
                response.status_code = status.HTTP_200_OK
                return user
            except Exception as e:
                return JSONResponse(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    content=self.default_error_response(str(e))
                )
            