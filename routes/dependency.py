from sqlalchemy.exc import IntegrityError, NoResultFound
from fastapi import APIRouter, Response, status, Depends
from fastapi.responses import JSONResponse
from interfaces.route_interface import RouteInterface
from interfaces.json.api_dtos import Dependencies as DependenciesJson, DependenciesPostJson
from services import DependencyService
from models import Dependencies, User
from fastapi_jwt_auth import AuthJWT

class DepdenciesAPI(RouteInterface):
    def __init__(self, session):
        super().__init__()
        self.session = session
        self.router = APIRouter()
        self.setup_routes()
        
        # Services
        self.service = DependencyService
        
    def setup_routes(self):
        @self.router.get("/dependencies/{dependencyId}")
        async def getDependencies(dependencyId: int, response: Response):
            try:
                dependency = Dependencies.getDependency(dependencyId)
                response.status_code = status.HTTP_200_OK
                if dependency == None:
                    raise NoResultFound(f"Dependency with ID {dependencyId} not found.")
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
                
        @self.router.get("/dependencies")
        async def getDependencies(response: Response, auth: AuthJWT = Depends()):
            try:
                userId = auth.get_jwt_subject()
                
                dependencies = self.service.getDependencies(userId)
                response.status_code = status.HTTP_200_OK
                if dependencies == None:
                    raise Exception("Not found.")
                return dependencies
            except Exception as e:
                return JSONResponse(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    content=self.default_error_response(str(e))
                )
                
        @self.router.post("/dependencies")
        async def postDependency(request: DependenciesPostJson, response: Response, auth: AuthJWT = Depends()):
            try:
                userId = auth.get_jwt_subject()
                
                self.service.dependency(userId, request)
                response.status_code = status.HTTP_200_OK
                return Dependencies.getDependencies()
            except Exception as e:
                return JSONResponse(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    content=self.default_error_response(str(e))
                )
                
        @self.router.patch("/dependencies/{dependencyId}")
        async def updateDependency(dependencyId: int, request: DependenciesJson, response: Response):
            try:
                dependency = self.service.updateDependency(dependencyId, request)
                response.status_code = status.HTTP_200_OK
                return dependency
            except Exception as e:
                return JSONResponse(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    content=self.default_error_response(str(e))
                )