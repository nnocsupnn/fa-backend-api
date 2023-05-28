import json
from sqlalchemy.exc import IntegrityError
from fastapi import APIRouter, Response, status, Depends
from fastapi.exceptions import FastAPIError
from fastapi.responses import JSONResponse
from models import IncomeProtection
from sqlalchemy.orm import joinedload
from interfaces.route_interface import RouteInterface
from interfaces.json import IncomeProtectionProvisionPostJson, IncomeProtectionPostJson, IncomeProtectionResponseJson, IncomeProtectionProvisionResponseJson, IncomeProtectionProvisionPatchJson
from services import IncomeProtectionService
from config.functions import serialize_model
from fastapi_jwt_auth import AuthJWT
from typing import Any, List
from config.functions import mapToObject
from fastapi.encoders import jsonable_encoder
'''
IncomeProtectionAPI Resource

@interface RouteInterface
@author Nino Casupanan
@memberof MediCard
'''
class IncomeProtectionAPI(RouteInterface):
    def __init__(self, session):
        super().__init__()
        self.session = session
        self.router = APIRouter()
        self.setup_routes()
        
        # Services
        self.service = IncomeProtectionService
    
    def setup_routes(self):
        @self.router.get("/income-protection", summary="Get Income protection")
        async def incomeProtections(response: Response, auth: AuthJWT = Depends()) -> IncomeProtectionResponseJson:
            auth.jwt_required()
            
            userId = auth.get_jwt_subject()
            
            incomeProtection = self.service.incomeProtections(userId)
            print(incomeProtection)
            res = mapToObject(incomeProtection, IncomeProtectionResponseJson)
            res.income_protection_provision = [mapToObject(prov, IncomeProtectionProvisionResponseJson) for prov in incomeProtection.income_protection_provision]
            return JSONResponse(content=jsonable_encoder(res), status_code=status.HTTP_200_OK)
        '''
        '''
        @self.router.post("/income-protection", summary="Save Income protection", description="Saving income protection. Note: Only 1 income protection is allowed per user.")
        async def incomeProtection(incomeProtection: IncomeProtectionPostJson, response: Response, auth: AuthJWT = Depends()) -> IncomeProtectionResponseJson:
            auth.jwt_required()
            
            userId = auth.get_jwt_subject()
            incomeProtection = self.service.saveIncomeProtection(incomeProtection, userId)
            res = mapToObject(incomeProtection, IncomeProtectionResponseJson)
            res.income_protection_provision = [mapToObject(prov, IncomeProtectionProvisionResponseJson) for prov in incomeProtection.income_protection_provision]
            
            return JSONResponse(content=jsonable_encoder(res), status_code=status.HTTP_201_CREATED)
        '''
        '''
        @self.router.post("/income-protection/{incomeProtectionId}/provision", summary="Save Income protection provision")
        async def incomeProtection(incomeProtectionId: int, incomeProtectionProvision: IncomeProtectionProvisionPostJson, response: Response) -> IncomeProtectionResponseJson:
            incomeProtection = self.service.saveIncomeProtectionProvision(incomeProtectionProvision, incomeProtectionId)
            
            res = mapToObject(incomeProtection, IncomeProtectionResponseJson)
            res.income_protection_provision = [mapToObject(prov, IncomeProtectionProvisionResponseJson) for prov in incomeProtection.income_protection_provision]
            return JSONResponse(content=jsonable_encoder(res), status_code=status.HTTP_201_CREATED)
        '''
        '''
        @self.router.patch("/income-protection/{incomeProtectionId}/provision/{incomeProtectionProvisionId}", summary="Update income protection provision")
        async def updateIncomeProtection(incomeProtectionId: int, incomeProtectionProvisionId: int, incomeProtectionJson: IncomeProtectionProvisionPatchJson, response: Response) -> IncomeProtectionProvisionResponseJson:
            incomeProtection = self.service.updateIncomeProtection(incomeProtectionId, incomeProtectionProvisionId, incomeProtectionJson)
            
            res = mapToObject(incomeProtection, IncomeProtectionProvisionResponseJson)
            return JSONResponse(content=jsonable_encoder(res), status_code=status.HTTP_202_ACCEPTED)
        '''
        '''
        @self.router.delete("/income-protection/{incomeProtectionId}/provision/{incomeProtectionProvisionId}", summary="Delete income protection provision")
        async def updateIncomeProtection(incomeProtectionId: int, incomeProtectionProvisionId: int, response: Response) -> IncomeProtectionProvisionResponseJson:
            self.service.deleteIncomeProtectionProvision(incomeProtectionId, incomeProtectionProvisionId)
            
            response.status_code = status.HTTP_204_NO_CONTENT
            return True