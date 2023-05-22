import json
from sqlalchemy.exc import IntegrityError
from fastapi import APIRouter, Response, status, Depends
from fastapi.exceptions import FastAPIError
from fastapi.responses import JSONResponse
from models import Expenses
from sqlalchemy.orm import joinedload
from interfaces.route_interface import RouteInterface
from interfaces.json import ExpenseResponseJson, ExpensePatchJson
from services import ExpensesServices
from config.functions import serialize_model
from fastapi_jwt_auth import AuthJWT
from typing import Any, List, Optional
from config.functions import mapToObject
'''
TextTemplateAPI Resource

@interface RouteInterface
@author Nino Casupanan
@memberof MediCard
'''
class ExpensesAPI(RouteInterface):
    def __init__(self, session):
        super().__init__()
        self.session = session
        self.router = APIRouter()
        self.setup_routes()
        
        # Services
        self.service = ExpensesServices
    
    def setup_routes(self):
        @self.router.get("/expenses", summary="Get all expenses")
        async def getExpenses(auth: AuthJWT = Depends()) -> List[ExpenseResponseJson]:
            auth.jwt_required()
            userId = auth.get_jwt_subject()
            expenses = self.service.getExpenses(userId)
            
            res = []
            for ex in expenses:
                res.append(mapToObject(ex, ExpenseResponseJson))
            
            return res
        '''
        '''      
        @self.router.get("/expense/{expenseId}", summary="Get expense")
        async def getExpense(expenseId: int) -> Optional[ExpenseResponseJson]:
            expense = self.service.getExpense(expenseId)
                
            objectResponse = mapToObject(expense, ExpenseResponseJson)
            return objectResponse

        '''
        '''
        @self.router.patch("/expense/{expenseId}", summary="Update expense")
        async def updateExpense(expenseId: int, patchData: ExpensePatchJson) -> ExpenseResponseJson:
            expense = self.service.updateExpense(expenseId, patchData)
            
            objectResponse = mapToObject(expense, ExpenseResponseJson)
            return objectResponse
        
        '''
        '''
        @self.router.delete("/expense/{expenseId}", summary="Delete expense", status_code=status.HTTP_204_NO_CONTENT, response_description="Deleted successfuly.")
        async def deleteExpense(expenseId: int, response: Response):
            self.service.deleteExpense(expenseId)
            
            response.status_code = status.HTTP_204_NO_CONTENT
            return True