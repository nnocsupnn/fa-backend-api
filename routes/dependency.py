from sqlalchemy.exc import IntegrityError, NoResultFound
from fastapi import APIRouter, Response, status, Depends
from fastapi.responses import JSONResponse
from interfaces.route_interface import RouteInterface
from interfaces.json import Dependencies as DependenciesJson, DependenciesPostJson, DependenciesResponseJsonFull, DependencyDetailResponseJson, DependencyProvisionResponseJson, DependenciesResponseJson
from services import DependencyService
from models import Dependencies, User
from fastapi_jwt_auth import AuthJWT
from config.functions import mapToObject, mapToObjectA
from typing import List
from fastapi.encoders import jsonable_encoder

class DepdenciesAPI(RouteInterface):
    def __init__(self, session):
        super().__init__()
        self.session = session
        self.router = APIRouter()
        self.setup_routes()
        
        # Services
        self.service = DependencyService
        
    def setup_routes(self):
        @self.router.get("/dependency/{dependencyId}", summary="Getting dependency")
        async def getDependencies(dependencyId: int, response: Response) -> DependenciesResponseJsonFull:
            dependency = Dependencies.getDependency(dependencyId)
            if dependency == None:
                raise NoResultFound(f"Dependency with ID {dependencyId} not found.")

            # res = mapToObjectA(dependency, DependenciesResponseJsonFull(), {
            #     "dependency_detail": DependencyDetailResponseJson(), 
            #     "dependency_provision": DependencyProvisionResponseJson()
            # }, DependenciesResponseJsonFull())
            
            res = mapToObject(dependency, DependenciesResponseJsonFull, DependencyDetailResponseJson, DependencyProvisionResponseJson)
            return JSONResponse(content=jsonable_encoder(res), status_code=status.HTTP_200_OK)
        '''
        '''  
        @self.router.get("/dependencies", summary="Listing dependencies")
        async def getDependencies(response: Response, auth: AuthJWT = Depends()) -> List[DependenciesResponseJson]:
            userId = auth.get_jwt_subject()
            
            dependencies = self.service.getDependencies(userId)
            if dependencies == None:
                raise Exception("Not found.")
            
            res = [mapToObject(dep, DependenciesResponseJsonFull, DependencyDetailResponseJson, DependencyProvisionResponseJson) for dep in dependencies]
            
            return JSONResponse(content=jsonable_encoder(res), status_code=status.HTTP_200_OK)
        '''
        '''
        @self.router.post("/dependency", summary="Adding Dependency", description="Adding dependency, please see the schema. This includes other property")
        async def postDependency(request: DependenciesPostJson, response: Response, auth: AuthJWT = Depends()) -> List[DependenciesResponseJson]:
            userId = auth.get_jwt_subject()
            self.service.dependency(userId, request)
            res = [mapToObject(dep, DependenciesResponseJsonFull, DependencyDetailResponseJson, DependencyProvisionResponseJson) for dep in Dependencies.getDependencies()]
            
            return JSONResponse(content=jsonable_encoder(res), status_code=status.HTTP_201_CREATED)
        '''
        '''     
        @self.router.patch("/dependency/{dependencyId}", summary="Updating dependency")
        async def updateDependency(dependencyId: int, request: DependenciesJson, response: Response):
            dependency = self.service.updateDependency(dependencyId, request)
            res = mapToObject(dependency, DependenciesResponseJsonFull, DependencyDetailResponseJson, DependencyProvisionResponseJson) if dependency != None else DependenciesResponseJson()
            return JSONResponse(content=jsonable_encoder(res), status_code=status.HTTP_200_OK)
        '''
        '''   
        @self.router.delete("/dependency/{dependencyId}", summary="Deleting dependency", description="Deleting dependency will also delete the detail and provision.")
        async def updateDependency(dependencyId: int, response: Response):
            dependency = self.service.deleteDependency(dependencyId)
            response.status_code = status.HTTP_204_NO_CONTENT
            return dependency