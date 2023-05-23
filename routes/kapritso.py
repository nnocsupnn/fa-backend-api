from sqlalchemy.exc import IntegrityError
from fastapi import APIRouter, Response, status, Depends
from fastapi.exceptions import FastAPIError
from fastapi.responses import JSONResponse
from models import LifestyleProtection, LifestyleProtectionInvestments
from sqlalchemy.orm import joinedload
from interfaces.route_interface import RouteInterface
from interfaces.json import KapritsoPatchJson, KapritsoResponseJson
from services import KapritsoService
from config.functions import serialize_model
from fastapi_jwt_auth import AuthJWT
from typing import Any, List
from config.functions import mapToObject
from fastapi.encoders import jsonable_encoder
'''
KapritsoAPI Resource

@interface RouteInterface
@author Nino Casupanan
@memberof MediCard
'''
class KapritsoAPI(RouteInterface):
    def __init__(self, session):
        super().__init__()
        self.session = session
        self.router = APIRouter()
        self.setup_routes()
        
        # Services
        self.service = KapritsoService
    
    def setup_routes(self):
        @self.router.get("/kapritso", summary="Get kapritso")
        async def getKapritso(response: Response, auth: AuthJWT = Depends()) -> KapritsoResponseJson:
            userId = auth.get_jwt_subject()
            kapritso = self.service.getKapritso(userId)
            res = mapToObject(kapritso, KapritsoResponseJson)
            return JSONResponse(content=jsonable_encoder(res), status_code=status.HTTP_200_OK)
        
        '''
        '''
        @self.router.patch("/kapritso", summary="Update kapritso")
        async def getKapritso(request: KapritsoPatchJson, response: Response, auth: AuthJWT = Depends()) -> KapritsoResponseJson:
            userId = auth.get_jwt_subject()
            kapritso = self.service.updateKapritso(userId, request)
            res = mapToObject(kapritso, KapritsoResponseJson)
            return JSONResponse(content=jsonable_encoder(res), status_code=status.HTTP_200_OK)