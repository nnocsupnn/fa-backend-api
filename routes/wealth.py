import json
from sqlalchemy.exc import IntegrityError
from fastapi import APIRouter, Response, status, Depends
from fastapi.exceptions import FastAPIError
from fastapi.responses import JSONResponse
from models import LifestyleProtection, LifestyleProtectionInvestments
from sqlalchemy.orm import joinedload
from interfaces.route_interface import RouteInterface
from interfaces.json import WealthPatchJson, WealthResponseJson
from services import WealthService
from config.functions import serialize_model
from fastapi_jwt_auth import AuthJWT
from typing import Any, List
from config.functions import mapToObject
from fastapi.encoders import jsonable_encoder
'''
WealthAPI Resource

@interface RouteInterface
@author Nino Casupanan
@memberof MediCard
'''
class WealthAPI(RouteInterface):
    def __init__(self, session):
        super().__init__()
        self.session = session
        self.router = APIRouter()
        self.setup_routes()
        
        # Services
        self.service = WealthService
    
    def setup_routes(self):
        @self.router.get("/wealth", summary="Get Wealth")
        async def getWealth(response: Response, auth: AuthJWT = Depends()) -> WealthResponseJson:
            userId = auth.get_jwt_subject()
            
            wealth = self.service.getWealths(userId)
            res = mapToObject(wealth, WealthResponseJson) if wealth != None else WealthResponseJson()
            return res
        '''
        '''
        @self.router.patch("/wealth/{wealthId}", summary="Update Wealth")
        async def getWealth(wealthId: int, request: WealthPatchJson, response: Response) -> WealthResponseJson:
            
            wealth = self.service.updateWealth(wealthId, request)
            res = mapToObject(wealth, WealthResponseJson) if wealth != None else WealthResponseJson()
            return JSONResponse(content=jsonable_encoder(res), status_code=status.HTTP_200_OK)