from sqlalchemy.exc import IntegrityError
from fastapi import APIRouter, Response, status, Depends
from fastapi.responses import JSONResponse
from interfaces.route_interface import RouteInterface
from services import DependencyService

class DepdenciesAPI(RouteInterface):
    def __init__(self, session):
        super().__init__()
        self.session = session
        self.router = APIRouter()
        self.setup_routes()
        
        # Services
        self.service = DependencyService
        
    def setup_routes(self):
        @self.router.get("/user/{id}/dependencies")
        async def getDependencies(id: int, response: Response):
            try:
                user = self.service.dependency(id)
               
                response.status_code = status.HTTP_200_OK
                return user
            except Exception as e:
                return JSONResponse(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    content=self.default_error_response(str(e))
                )