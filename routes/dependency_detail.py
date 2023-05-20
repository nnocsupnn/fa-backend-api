from fastapi import APIRouter
from sqlalchemy.exc import IntegrityError, NoResultFound
from fastapi import APIRouter, Response, status, Depends
from fastapi.responses import JSONResponse
from interfaces.route_interface import RouteInterface
from interfaces.json import DependencyDetailPostJson, DependencyDetail as DependencyDetailJson, DependenciesResponseJson, DependencyDetailResponseJson, DependencyProvisionResponseJson
from services import DependencyDetailService
from models import DependencyDetail
from config.functions import mapToObject

class DepdencyDetailAPI(RouteInterface):
    def __init__(self, session):
        super().__init__()
        self.session = session
        self.router = APIRouter()
        self.setup_routes()
        
        # Services
        self.service = DependencyDetailService
        
    def setup_routes(self):
        @self.router.get("/dependency/{dependencyId}/detail")
        async def getDependencies(dependencyId: int, response: Response) -> DependencyDetailResponseJson:
            dependency = self.service.getDependencyDetail(dependencyId)
            response.status_code = status.HTTP_200_OK
            if dependency == None:
                raise NoResultFound(f"DependencyDetail with ID {dependencyId} not found.")
            
            res = mapToObject(dependency, DependencyDetailResponseJson, DependencyProvisionResponseJson)
            return res
        
        @self.router.post("/dependency/{dependencyId}/detail")
        async def createDependencyDetail(dependencyId: int, request: DependencyDetailPostJson, response: Response) -> DependenciesResponseJson:
            dependency = self.service.save(dependencyId, request)
            response.status_code = status.HTTP_201_CREATED
            if dependency == None:
                raise NoResultFound(f"DependencyDetail with ID {dependencyId} not found.")
            
            res = mapToObject(dependency, DependenciesResponseJson)
            return res
                
        @self.router.patch("/dependency/{dependencyId}/detail")
        async def updateDependencyDetail(dependencyId: int, request: DependencyDetailJson, response: Response) -> DependenciesResponseJson:
            dependency = self.service.updateDependency(dependencyId, request)
            response.status_code = status.HTTP_200_OK
            if dependency == None:
                raise NoResultFound(f"DependencyDetail with ID {dependencyId} not found.")
            return dependency