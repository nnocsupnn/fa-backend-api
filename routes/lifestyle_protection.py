import json
from sqlalchemy.exc import IntegrityError
from fastapi import APIRouter, Response, status, Depends
from fastapi.exceptions import FastAPIError
from fastapi.responses import JSONResponse
from models import LifestyleProtection, LifestyleProtectionInvestments
from sqlalchemy.orm import joinedload
from interfaces.route_interface import RouteInterface
from interfaces.json import LifestyleProtectionPatchJson, \
    LifestyleProtectionInvestmentsPostJson, \
    LifestyleProtectionInvestmentsPatchJson, \
    LifestyleProtectionInvestmentsResponseJson, \
    LifestyleProtectionResponseJson
from services import LifestyleProtectionService
from config.functions import serialize_model
from fastapi_jwt_auth import AuthJWT
from typing import Any, List
from config.functions import mapToObject
from fastapi.encoders import jsonable_encoder
'''
LifestyleProtectionAPI Resource

@interface RouteInterface
@author Nino Casupanan
@memberof MediCard
'''
class LifestyleProtectionAPI(RouteInterface):
    def __init__(self, session):
        super().__init__()
        self.session = session
        self.router = APIRouter()
        self.setup_routes()
        
        # Services
        self.service = LifestyleProtectionService
    
    def setup_routes(self):
        '''
        Lifestyle Protection
        '''
        @self.router.get("/lifestyle-protection", summary="Get lifestyle protection")
        async def getLifestyleProtection(response: Response, auth: AuthJWT = Depends()) -> LifestyleProtectionResponseJson:
            auth.jwt_required()
            
            userId = auth.get_jwt_subject()
            protection = self.service.getProtections(userId)
            res = mapToObject(protection, LifestyleProtectionResponseJson)
            
            return JSONResponse(content=jsonable_encoder(res), status_code=status.HTTP_200_OK)
        '''
        '''
        @self.router.patch("/lifestyle-protection", summary="Update lifestyle protection")
        async def updateLifestyleProtection(request: LifestyleProtectionPatchJson, response: Response, auth: AuthJWT = Depends()) -> LifestyleProtectionResponseJson or None:
            auth.jwt_required()
            
            userId = auth.get_jwt_subject()
            protection = self.service.update(userId, request)
            res = mapToObject(protection, LifestyleProtectionResponseJson)
            
            return JSONResponse(content=jsonable_encoder(res), status_code=status.HTTP_200_OK)
        '''
        Lifestyle Protection Investments
        '''
        @self.router.get("/lifestyle-protection/investment/{investmentId}", summary="Update lifestyle protection investments")
        async def updateLifestyleProtectionInvestments(investmentId: int, response: Response) -> LifestyleProtectionInvestmentsResponseJson:
            investment = self.service.getInvestmentsById(investmentId)
            res = mapToObject(investment, LifestyleProtectionInvestmentsResponseJson)
            
            return JSONResponse(content=jsonable_encoder(res), status_code=status.HTTP_200_OK)
        '''
        '''
        @self.router.patch("/lifestyle-protection/investment/{investmentId}", summary="Update lifestyle protection investments")
        async def updateLifestyleProtectionInvestments(investmentId: int, request: LifestyleProtectionInvestmentsPatchJson, response: Response) -> LifestyleProtectionInvestmentsResponseJson:
            investment = self.service.updateInvestment(investmentId, request)
            res = mapToObject(investment, LifestyleProtectionInvestmentsResponseJson)
            
            return JSONResponse(content=jsonable_encoder(res), status_code=status.HTTP_200_OK)
        
        '''
        '''
        @self.router.post("/lifestyle-protection/investment", summary="Add lifestyle protection investments")
        async def saveLifestyleProtectionInvestments(request: LifestyleProtectionInvestmentsPostJson, response: Response, auth: AuthJWT = Depends()) -> LifestyleProtectionInvestmentsResponseJson:
            auth.jwt_required()
            
            userId = auth.get_jwt_subject()
            
            investment = self.service.saveInvestment(userId, request)
            res = mapToObject(investment, LifestyleProtectionInvestmentsResponseJson)
            return JSONResponse(content=jsonable_encoder(res), status_code=status.HTTP_201_CREATED)
        '''
        '''
        @self.router.get("/lifestyle-protection/investments", summary="Get lifestyle protection investments")
        async def getLifestyleProtectionInvestments(response: Response, auth: AuthJWT = Depends()) -> List[LifestyleProtectionInvestmentsResponseJson]:
            auth.jwt_required()
            
            userId = auth.get_jwt_subject()
            investments = self.service.getInvestments(userId)
            res = [mapToObject(investment, LifestyleProtectionInvestmentsResponseJson) for investment in investments]
            return JSONResponse(content=jsonable_encoder(res), status_code=status.HTTP_200_OK)
        