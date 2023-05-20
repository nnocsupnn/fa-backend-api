import json
from fastapi import APIRouter, Response, status, Depends
from fastapi.exceptions import FastAPIError
from fastapi.responses import JSONResponse
from models import User
from sqlalchemy.orm import joinedload
from interfaces.route_interface import RouteInterface
from interfaces.json.api_dtos import User as UserJson, UserDetail as UserDetailJson
from services import UserDetailService
from config.functions import serialize_model
from fastapi_jwt_auth import AuthJWT
import jwt
'''
UserAPI is class for User Resource

@interface RouteInterface
@author Nino Casupanan
@memberof MediCard
'''
class UserDetailAPI(RouteInterface):
    def __init__(self, session):
        super().__init__()
        self.session = session
        self.router = APIRouter()
        self.setup_routes()
        
        # Services
        self.service = UserDetailService
        
    def setup_routes(self):
        
        @self.router.get("/user/current/detail", summary="Get current user detail")
        async def getCurrentUserDetail(response: Response, auth: AuthJWT = Depends()):
            auth.jwt_required()
            userId = auth.get_jwt_subject()
            
            user = self.service.getDetail(userId)
            
            response.status_code = status.HTTP_200_OK
            return user
                
        '''
        '''   
        @self.router.patch("/user/current/detail", summary="Get current user detail")
        async def updateCurrentDetail(request: UserDetailJson, response: Response, auth: AuthJWT = Depends()):
            auth.jwt_required()
            userId = auth.get_jwt_subject()
            user = self.service.update(userId, request)
            
            response.status_code = status.HTTP_200_OK
            return user
        '''
        '''       
        @self.router.get("/user/{id}/detail", summary="Get user's detail")
        async def getDetail(id: int, response: Response):
            user = self.service.getDetail(id)
            
            response.status_code = status.HTTP_200_OK
            return user
        '''
        '''      
        @self.router.patch("/user/{id}/detail", summary="Update user's detail")
        async def getDetail(id: int, request: UserDetailJson, response: Response):
            user = self.service.update(id, request)
            
            response.status_code = status.HTTP_200_OK
            return user