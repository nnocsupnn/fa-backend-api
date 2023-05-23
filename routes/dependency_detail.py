from fastapi import APIRouter
from sqlalchemy.exc import IntegrityError, NoResultFound
from fastapi import APIRouter, Response, status, Depends
from fastapi.responses import JSONResponse
from interfaces.route_interface import RouteInterface
from interfaces.json import DependencyDetailPostJson, DependencyDetail as DependencyDetailJson, DependenciesResponseJson, DependencyDetailResponseJson, DependencyProvisionResponseJson
from services import DependencyDetailService
from models import DependencyDetail
from config.functions import mapToObject
from fastapi.encoders import jsonable_encoder

class DepdencyDetailAPI(RouteInterface):
    def __init__(self, session):
        super().__init__()
        self.session = session
        self.router = APIRouter()
        self.setup_routes()
        
        # Services
        self.service = DependencyDetailService
        
    def setup_routes(self):
        @self.router.get("/dependency/{dependencyId}/detail", summary="Get the dependency details")
        async def getDependencies(dependencyId: int, response: Response) -> DependencyDetailResponseJson:
            dependency = self.service.getDependencyDetail(dependencyId)
            if dependency == None:
                raise NoResultFound(f"DependencyDetail with ID {dependencyId} not found.")
            
            res = mapToObject(dependency, DependencyDetailResponseJson, DependencyProvisionResponseJson)
            return JSONResponse(content=jsonable_encoder(res), status_code=status.HTTP_200_OK)
        '''
        '''
        @self.router.post("/dependency/{dependencyId}/detail", summary="Add dependency details")
        async def createDependencyDetail(dependencyId: int, request: DependencyDetailPostJson, response: Response) -> DependenciesResponseJson:
            dependency = self.service.save(dependencyId, request)
            
            if dependency == None:
                raise NoResultFound(f"DependencyDetail with ID {dependencyId} not found.")
            
            res = mapToObject(dependency, DependenciesResponseJson)
            return JSONResponse(content=jsonable_encoder(res), status_code=status.HTTP_201_CREATED)
        '''
        '''
        @self.router.patch("/dependency/{dependencyId}/detail", summary="Update dependency detail")
        async def updateDependencyDetail(dependencyId: int, request: DependencyDetailJson, response: Response) -> DependencyDetailResponseJson:
            dependency = self.service.updateDependency(dependencyId, request)
            response.status_code = status.HTTP_200_OK
            if dependency == None:
                raise NoResultFound(f"DependencyDetail with ID {dependencyId} not found.")
            
            res = mapToObject(dependency, DependencyDetailResponseJson, DependencyProvisionResponseJson)
            return JSONResponse(content=jsonable_encoder(res), status_code=status.HTTP_200_OK)