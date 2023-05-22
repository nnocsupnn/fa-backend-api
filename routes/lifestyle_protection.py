import json
from sqlalchemy.exc import IntegrityError
from fastapi import APIRouter, Response, status, Depends
from fastapi.exceptions import FastAPIError
from fastapi.responses import JSONResponse
from models import LifestyleProtection, LifestyleProtectionInvestments
from sqlalchemy.orm import joinedload
from interfaces.route_interface import RouteInterface
from interfaces.json import IncomeProtectionProvisionPostJson
from services import LifestyleProtectionService
from config.functions import serialize_model
from fastapi_jwt_auth import AuthJWT
from typing import Any, List
from config.functions import mapToObject
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
        @self.router.get("/lifestyle-protection", summary="Get lifestyle protection")
        async def getLifestyleProtection():
            pass