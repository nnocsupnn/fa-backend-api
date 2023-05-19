from fastapi import APIRouter
from sqlalchemy.exc import IntegrityError, NoResultFound
from fastapi import APIRouter, Response, status, Depends
from fastapi.responses import JSONResponse
from interfaces.route_interface import RouteInterface
from interfaces.json.api_dtos import DependencyDetailPostJson, DependencyDetail as DependencyDetailJson
from services import DependencyDetailService
from models import DependencyDetail

class DepdencyDetailAPI(RouteInterface):
    def __init__(self, session):
        super().__init__()
        self.session = session
        self.router = APIRouter()
        self.setup_routes()
        
        # Services
        self.service = DependencyDetailService
        
    def setup_routes(self):
        @self.router.get("/dependencies/{dependencyId}/detail")
        async def getDependencies(dependencyId: int, response: Response):
            try:
                dependency = self.service.getDependencyDetail(dependencyId)
                response.status_code = status.HTTP_200_OK
                if dependency == None:
                    raise NoResultFound(f"DependencyDetail with ID {dependencyId} not found.")
                return dependency
            except NoResultFound as e:
                return JSONResponse(
                    status_code=status.HTTP_404_NOT_FOUND,
                    content=self.default_error_response(str(e), status.HTTP_404_NOT_FOUND)
                )
            except Exception as e:
                return JSONResponse(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    content=self.default_error_response(str(e))
                )
        
        @self.router.post("/dependencies/{dependencyId}/detail")
        async def createDependencyDetail(dependencyId: int, request: DependencyDetailPostJson, response: Response):
            try:
                dependency = self.service.save(dependencyId, request)
                response.status_code = status.HTTP_201_CREATED
                if dependency == None:
                    raise NoResultFound(f"DependencyDetail with ID {dependencyId} not found.")
                return dependency
            except NoResultFound as e:
                return JSONResponse(
                    status_code=status.HTTP_404_NOT_FOUND,
                    content=self.default_error_response(str(e), status.HTTP_404_NOT_FOUND)
                )
            except Exception as e:
                return JSONResponse(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    content=self.default_error_response(str(e))
                )
                
        @self.router.patch("/dependencies/{dependencyId}/detail")
        async def updateDependencyDetail(dependencyId: int, request: DependencyDetailJson, response: Response):
            try:
                dependency = self.service.updateDependency(dependencyId, request)
                response.status_code = status.HTTP_200_OK
                if dependency == None:
                    raise NoResultFound(f"DependencyDetail with ID {dependencyId} not found.")
                return dependency
            except NoResultFound as e:
                return JSONResponse(
                    status_code=status.HTTP_404_NOT_FOUND,
                    content=self.default_error_response(str(e), status.HTTP_404_NOT_FOUND)
                )
            except Exception as e:
                return JSONResponse(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    content=self.default_error_response(str(e))
                )