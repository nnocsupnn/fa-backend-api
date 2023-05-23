import json
from fastapi import APIRouter, Response, status, Depends
from fastapi.exceptions import FastAPIError
from fastapi.responses import JSONResponse
from models import User
from sqlalchemy.orm import joinedload
from interfaces.route_interface import RouteInterface
from interfaces.json import TextTemplate as TextTemplateJson, TextTemplatesResponseJson, Categories
from services import TextTemplateService
from config.functions import serialize_model, mapToObject
from fastapi_jwt_auth import AuthJWT
from typing import List 
from fastapi.encoders import jsonable_encoder
'''
TextTemplateAPI Resource

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
        @self.router.get("/templates", summary="Get all available templates")
        def templates() -> List[TextTemplatesResponseJson]:
            templates = self.service.templates()
            res = [mapToObject(val, TextTemplatesResponseJson) for val in templates]
            return JSONResponse(content=jsonable_encoder(res), status_code=status.HTTP_200_OK)
            
        @self.router.get("/template/{code}", summary="Get template by code")
        def template(code: str) -> TextTemplatesResponseJson:
            template = self.service.template(subj=code)
            res = mapToObject(template, TextTemplatesResponseJson)
            return JSONResponse(content=jsonable_encoder(res), status_code=status.HTTP_200_OK)
            
        @self.router.post("/template", summary="Add template")
        def template(tt: TextTemplateJson) -> TextTemplatesResponseJson:
            result = self.service.save(tt)
            res = mapToObject(result, TextTemplatesResponseJson)
            return JSONResponse(content=jsonable_encoder(res), status_code=status.HTTP_201_CREATED)
        
        @self.router.get("/template/category/{category}", summary="Get template by category")
        def template(category: Categories) -> List[TextTemplatesResponseJson]:
            templates = self.service.templatesByCategory(category=category)
            res = [mapToObject(val, TextTemplatesResponseJson) for val in templates]
            return JSONResponse(content=jsonable_encoder(res), status_code=status.HTTP_200_OK)
            
        @self.router.delete("/template/{code}", summary="Deleting template by Code", status_code=status.HTTP_204_NO_CONTENT)
        def template(code: str, response: Response):
            self.service.delete(code)
            response.status_code = status.HTTP_204_NO_CONTENT