import json
from sqlalchemy.exc import IntegrityError
from fastapi import APIRouter, Response, status, Depends
from fastapi.exceptions import FastAPIError
from fastapi.responses import JSONResponse
from models import User
from sqlalchemy.orm import joinedload
from interfaces.route_interface import RouteInterface
from interfaces.json import User as UserJson, \
    UserResponseJson, \
    LifestyleProtectionResponseJson, \
    LifestyleProtectionInvestmentsResponseJson, \
    KapritsoResponseJson, \
    WealthResponseJson, \
    UserDetailResponseJson, \
    OccupationResponseJson, \
    DependenciesResponseJson, \
    IncomeProtectionResponseJson, \
    ExpenseResponseJson, \
    IncomeResponseJson, \
    DependenciesResponseJsonFull, \
    DependencyDetailResponseJson, \
    DependencyProvisionResponseJson, \
    IncomeProtectionProvisionResponseJson, \
    UpdatePasswordPatchJson, \
    SuccessResponseJson
from services import UserService
from config.functions import serialize_model
from fastapi_jwt_auth import AuthJWT
from typing import List
from config.functions import mapToObject
from fastapi.encoders import jsonable_encoder
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
    def mapToUserResponse(self, user):
        res = mapToObject(user, UserResponseJson)
        res.kapritso = mapToObject(user.kapritso, KapritsoResponseJson) if user.kapritso != None else None
        res.wealth = mapToObject(user.wealth, WealthResponseJson) if user.wealth != None else None
        res.user_detail = mapToObject(user.user_detail, UserDetailResponseJson) if user.user_detail != None else None
        res.occupation = mapToObject(user.occupation, OccupationResponseJson) if user.occupation != None else None
        res.dependencies = [mapToObject(dependecny, DependenciesResponseJsonFull, DependencyDetailResponseJson, DependencyProvisionResponseJson) for dependecny in user.dependencies] if user.dependencies != None else None
        res.lifestyle_protection = mapToObject(user.lifestyle_protection, LifestyleProtectionResponseJson) if user.lifestyle_protection != None else None
        res.lifestyle_protection_investments = [mapToObject(lifestyle_protection_investment, LifestyleProtectionInvestmentsResponseJson) for lifestyle_protection_investment in user.lifestyle_protection_investments] if user.dependencies != None else None
        res.income_protection = mapToObject(user.income_protection, IncomeProtectionResponseJson) if user.income_protection != None else None
        res.income_protection.income_protection_provision = [mapToObject(prov, IncomeProtectionProvisionResponseJson) for prov in user.income_protection.income_protection_provision]
        
        return res
    
    def setup_routes(self):
        # Route Methodss
        @self.router.patch("/user/me", summary="Update current user")
        async def updateUser(request: UserJson, response: Response, auth: AuthJWT = Depends()):
            userId = auth.get_jwt_subject()
            user = self.service.updateUser(userId, request)
            response.status_code = status.HTTP_200_OK
            return user
        
        @self.router.get("/user/me", summary="Get current user")
        async def me(auth: AuthJWT = Depends()) -> UserResponseJson:
            userId = auth.get_jwt_subject()
            user = User.get_user(user_id=userId)
            
            res = self.mapToUserResponse(user)
            res.user_detail.expenses =  [mapToObject(val, ExpenseResponseJson) for val in user.user_detail.expenses]
            res.user_detail.incomes =  [mapToObject(val, IncomeResponseJson) for val in user.user_detail.incomes]

            return JSONResponse(content=jsonable_encoder(res), status_code=status.HTTP_200_OK)
        
        @self.router.get("/users", summary="Get all users", description="Note: this route is for `admin` role user.")
        async def getUsers(auth: AuthJWT = Depends()) -> List[UserResponseJson]:
            userId = auth.get_jwt_subject()
            user = User.get_user(user_id=userId)
            
            # if not user.user_level.__eq__("admin"):
            #     raise Exception("You are not allowed on this path.")
            
            users = User.get_users()
            res = [self.mapToUserResponse(user) for user in users]
            return JSONResponse(content=jsonable_encoder(res), status_code=status.HTTP_200_OK)
        
        
        @self.router.get("/user/{id}", summary="Get user", description="Note: this route is for `admin` role user.")
        async def getUser(id: int, response: Response) -> UserResponseJson:
            user = self.service.getUser(id)
               
            # if not user.user_level.__eq__("admin"):
            #     raise Exception("You are not allowed on this path.")
            
            '''
            Get user
            '''
            res = self.mapToUserResponse(user)
            res.user_detail.expenses =  [mapToObject(val, ExpenseResponseJson) for val in user.user_detail.expenses]
            res.user_detail.incomes =  [mapToObject(val, IncomeResponseJson) for val in user.user_detail.incomes]
            
            return JSONResponse(content=jsonable_encoder(res), status_code=status.HTTP_200_OK)
                
        
                
        @self.router.patch("/user/{id}", summary="Update user")
        async def updateUser(id: int, request: UserJson, response: Response) -> UserResponseJson:
            user = self.service.updateUser(id, request)
            response.status_code = status.HTTP_200_OK
            res = self.mapToUserResponse(user)
            return JSONResponse(content=jsonable_encoder(res), status_code=status.HTTP_200_OK)
            
        @self.router.delete("/user/{id}", summary="Delete user", status_code=status.HTTP_204_NO_CONTENT)
        async def deleteUser(id: int, response: Response) -> None:
            user = self.service.deleteUser(id)
            return JSONResponse(content=jsonable_encoder(user), status_code=status.HTTP_204_NO_CONTENT)
        
        
        @self.router.patch("/update-password", summary="Update Password")
        async def updatePassword(body: UpdatePasswordPatchJson, response: Response, auth: AuthJWT = Depends()) -> SuccessResponseJson:
            auth.jwt_required()
            userId = auth.get_jwt_subject()
            self.service.updatePassword(body, userId)
            response.status_code = status.HTTP_202_ACCEPTED
            return SuccessResponseJson(status=status.HTTP_202_ACCEPTED, message="Password updated successfully.")