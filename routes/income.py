import json
from sqlalchemy.exc import IntegrityError
from fastapi import APIRouter, Response, status, Depends
from fastapi.exceptions import FastAPIError
from fastapi.responses import JSONResponse
from models import Incomes
from sqlalchemy.orm import joinedload
from interfaces.route_interface import RouteInterface
from interfaces.json import IncomePatchJson, Income, IncomeResponseJson, IncomePostJson
from services import IncomeService
from config.functions import serialize_model
from fastapi_jwt_auth import AuthJWT
from typing import Any, List
from config.functions import mapToObject
from fastapi.encoders import jsonable_encoder
'''
IncomeAPI Resource

@interface RouteInterface
@author Nino Casupanan
@memberof MediCard
'''
class IncomeAPI(RouteInterface):
    def __init__(self, session):
        super().__init__()
        self.session = session
        self.router = APIRouter()
        self.setup_routes()
        
        # Services
        self.service = IncomeService
    
    def setup_routes(self):
        @self.router.get("/incomes", summary="Get all incomes")
        async def getIncomes(response: Response, auth: AuthJWT = Depends()) -> List[IncomeResponseJson]:
            auth.jwt_required()
            userId = auth.get_jwt_subject()
            income = self.service.getIncomes(userId)
            
            res = []
            for ic in income:
                res.append(mapToObject(ic, IncomeResponseJson))
            
            return JSONResponse(content=jsonable_encoder(res), status_code=status.HTTP_200_OK)
        '''
        ''' 
        @self.router.post("/income", summary="Add income")
        async def getIncome(request: IncomePostJson, auth: AuthJWT = Depends()) -> IncomeResponseJson:
            auth.jwt_required()
            userId = auth.get_jwt_subject()
            income = self.service.saveIncome(userId, request)
            
            res = mapToObject(income, IncomeResponseJson)
            return JSONResponse(content=jsonable_encoder(res), status_code=status.HTTP_201_CREATED)
        '''
        '''
        @self.router.get("/income/{incomeId}", summary="Get income")
        async def getIncome(incomeId: int) -> IncomeResponseJson:
            income = self.service.getIncome(incomeId)
            
            objectResponse = mapToObject(income, IncomeResponseJson)
            return JSONResponse(content=jsonable_encoder(objectResponse), status_code=status.HTTP_200_OK)
        '''
        '''       
        @self.router.patch("/income/{incomeId}", summary="Update income")
        async def updateIncome(incomeId: int, patchData: IncomePatchJson) -> IncomeResponseJson:
            income = self.service.updateIncome(incomeId, patchData)
            
            objectResponse = mapToObject(income, IncomeResponseJson)
            return JSONResponse(content=jsonable_encoder(objectResponse), status_code=status.HTTP_200_OK)
        '''
        '''     
        @self.router.delete("/income/{incomeId}", summary="Delete income", status_code=status.HTTP_204_NO_CONTENT, response_description="Deleted successfuly.")
        async def deleteIncome(incomeId: int, response: Response):
            self.service.deleteIncome(incomeId)
            
            response.status_code = status.HTTP_204_NO_CONTENT
            return True