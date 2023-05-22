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
            try:
                dependency = Dependencies.getDependency(dependencyId)
                response.status_code = status.HTTP_200_OK
                if dependency == None:
                    raise NoResultFound(f"Dependency with ID {dependencyId} not found.")

                # res = mapToObjectA(dependency, DependenciesResponseJsonFull(), {
                #     "dependency_detail": DependencyDetailResponseJson(), 
                #     "dependency_provision": DependencyProvisionResponseJson()
                # }, DependenciesResponseJsonFull())
                
                res = mapToObject(dependency, DependenciesResponseJsonFull, DependencyDetailResponseJson, DependencyProvisionResponseJson)
                return res
            except NoResultFound as e:
                return JSONResponse(
                    status_code=status.HTTP_404_NOT_FOUND,
                    content=self.default_error_response(str(e), status.HTTP_404_NOT_FOUND)
                )
        '''
        '''  
        @self.router.get("/dependencies", summary="Listing dependencies")
        async def getDependencies(response: Response, auth: AuthJWT = Depends()) -> List[DependenciesResponseJson]:
            userId = auth.get_jwt_subject()
            
            dependencies = self.service.getDependencies(userId)
            res = [mapToObject(dep, DependenciesResponseJson) for dep in dependencies]
            response.status_code = status.HTTP_200_OK
            if dependencies == None:
                raise Exception("Not found.")
            return res
        '''
        '''
        @self.router.post("/dependency", summary="Adding Dependency", description="Adding dependency, please see the schema. This includes other property")
        async def postDependency(request: DependenciesPostJson, response: Response, auth: AuthJWT = Depends()) -> List[DependenciesResponseJson]:
            userId = auth.get_jwt_subject()
            self.service.dependency(userId, request)
            response.status_code = status.HTTP_200_OK
            res = [mapToObject(dep, DependenciesResponseJson) for dep in Dependencies.getDependencies()]
            return res
        '''
        '''     
        @self.router.patch("/dependency/{dependencyId}", summary="Updating dependency")
        async def updateDependency(dependencyId: int, request: DependenciesJson, response: Response):
            dependency = self.service.updateDependency(dependencyId, request)
            response.status_code = status.HTTP_204_NO_CONTENT
            return dependency
        '''
        '''   
        @self.router.delete("/dependency/{dependencyId}", summary="Deleting dependency", description="Deleting dependency will also delete the detail and provision.")
        async def updateDependency(dependencyId: int, response: Response):
            dependency = self.service.deleteDependency(dependencyId)
            response.status_code = status.HTTP_200_OK
            return dependency