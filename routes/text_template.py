import json
from fastapi import APIRouter, Response, status, Depends
from fastapi.exceptions import FastAPIError
from fastapi.responses import JSONResponse
from models import User
from sqlalchemy.orm import joinedload
from interfaces.route_interface import RouteInterface
from interfaces.json.api_dtos import TextTemplate as TextTemplateJson
from services import TextTemplateService
from config.functions import serialize_model
from fastapi_jwt_auth import AuthJWT
import jwt
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
        def templates():
            try:
                templates = self.service.templates()
                return templates
            except Exception as e:
                return self.default_error_response(str(e))
            
        @self.router.get("/template/{code}")
        def template(code: str):
            try:
                templates = self.service.template(subj=code)
                return templates
            except Exception as e:
                return self.default_error_response(str(e))
            
        @self.router.post("/template")
        def template(tt: TextTemplateJson):
            try:
                result = self.service.save(tt)
                return result
            except Exception as e:
                return self.default_error_response(str(e))