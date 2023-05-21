import json
from fastapi import APIRouter, Response, status, Depends
from fastapi.exceptions import FastAPIError
from fastapi.responses import JSONResponse
from models import User
from sqlalchemy.orm import joinedload
from interfaces.route_interface import RouteInterface
from interfaces.json import TextTemplate as TextTemplateJson, TextTemplatesResponseJson
from services import TextTemplateService
from config.functions import serialize_model, mapToObject
from fastapi_jwt_auth import AuthJWT
from typing import List 
'''
UserAPI is class for User Resource

@interface RouteInterface
@author Nino Casupanan
@memberof MediCard
'''
class TextTemplateAPI(RouteInterface):
    def __init__(self, session):
        super().__init__()
        self.session = session
        self.router = APIRouter()
        self.setup_routes()
        
        # Services
        self.service = TextTemplateService
        
    def setup_routes(self):
        @self.router.get("/templates")
        def templates() -> List[TextTemplatesResponseJson]:
            templates = self.service.templates()
            res = [mapToObject(val, TextTemplatesResponseJson) for val in templates]
            
            return res
            
        @self.router.get("/template/{code}")
        def template(code: str) -> TextTemplatesResponseJson:
            template = self.service.template(subj=code)
            res = mapToObject(template, TextTemplatesResponseJson)
            return res
            
        @self.router.post("/template")
        def template(tt: TextTemplateJson):
            result = self.service.save(tt)
            return result
            
        @self.router.delete("/template", summary="Deleting template", status_code=status.HTTP_204_NO_CONTENT)
        def template(code: str, response: Response):
            self.service.delete(code)
            response.status_code = status.HTTP_204_NO_CONTENT