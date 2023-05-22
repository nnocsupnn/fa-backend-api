import json
from sqlalchemy.exc import IntegrityError
from fastapi import APIRouter, Response, status, Depends
from fastapi.exceptions import FastAPIError
from fastapi.responses import JSONResponse
from models import IncomeProtection
from sqlalchemy.orm import joinedload
from interfaces.route_interface import RouteInterface
from interfaces.json import IncomePatchJson, Income, IncomeProtectionResponseJson
from services import IncomeProtectionService
from config.functions import serialize_model
from fastapi_jwt_auth import AuthJWT
from typing import Any, List
from config.functions import mapToObject
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
        @self.router.get("/income-protections", summary="Get Income protections")
        async def incomeProtections(response: Response, auth: AuthJWT = Depends()) -> List[IncomeProtectionResponseJson]:
            auth.jwt_required()
            
            userId = auth.get_jwt_subject()
            
            incomeProtections = self.service.incomeProtections(userId)
            res = [mapToObject(incomeProtection, IncomeProtectionResponseJson) for incomeProtection in incomeProtections]
            return res