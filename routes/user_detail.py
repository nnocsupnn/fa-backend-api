import json
from fastapi import APIRouter, Response, status, Depends
from fastapi.exceptions import FastAPIError
from fastapi.responses import JSONResponse
from models import User
from sqlalchemy.orm import joinedload
from interfaces.route_interface import RouteInterface
from interfaces.json import User as UserJson, UserDetail as UserDetailJson, UserDetailResponseJson, ExpenseResponseJson, IncomeResponseJson
from services import UserDetailService
from config.functions import serialize_model, mapToObject
from fastapi_jwt_auth import AuthJWT
from fastapi.encoders import jsonable_encoder 
'''
TextTemplateAPI Resource

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
        async def getCurrentUserDetail(response: Response, auth: AuthJWT = Depends()) -> UserDetailResponseJson:
            auth.jwt_required()
            userId = auth.get_jwt_subject()
            
            user = self.service.getDetail(userId)
            
            res = UserDetailResponseJson
            res = mapToObject(user, res)
            res.expenses =  [mapToObject(val, ExpenseResponseJson) for val in user.expenses]
            res.incomes =  [mapToObject(val, IncomeResponseJson) for val in user.incomes]
            
            return JSONResponse(content=jsonable_encoder(res), status_code=status.HTTP_200_OK)
                
        '''
        '''   
        @self.router.patch("/user/current/detail", summary="Get current user detail")
        async def updateCurrentDetail(request: UserDetailJson, response: Response, auth: AuthJWT = Depends()):
            auth.jwt_required()
            userId = auth.get_jwt_subject()
            user = self.service.update(userId, request)
            
            return JSONResponse(content=jsonable_encoder(user), status_code=status.HTTP_200_OK)
        '''
        '''       
        @self.router.get("/user/{id}/detail", summary="Get user's detail")
        async def getDetail(id: int, response: Response) -> UserDetailResponseJson:
            user = self.service.getDetail(id)
            
            res = UserDetailResponseJson
            res = mapToObject(user, res)
            res.expenses =  [mapToObject(val, ExpenseResponseJson) for val in user.expenses] if user.expenses != None else []
            res.incomes =  [mapToObject(val, IncomeResponseJson) for val in user.incomes] if user.incomes != None else []
            
            return JSONResponse(content=jsonable_encoder(res), status_code=status.HTTP_200_OK)
        '''
        '''      
        @self.router.patch("/user/{id}/detail", summary="Update user's detail")
        async def getDetail(id: int, request: UserDetailJson, response: Response) -> UserDetailResponseJson:
            user = self.service.update(id, request)
            
            response.status_code = status.HTTP_200_OK
            res = mapToObject(user, UserDetailResponseJson)
            res.expenses =  [mapToObject(val, ExpenseResponseJson) for val in user.expenses] if user.expenses != None else []
            res.incomes =  [mapToObject(val, IncomeResponseJson) for val in user.incomes] if user.incomes != None else []
            return JSONResponse(content=jsonable_encoder(res), status_code=status.HTTP_200_OK)