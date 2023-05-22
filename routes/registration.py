from interfaces.route_interface import RouteInterface
from fastapi import APIRouter, Response, status
from fastapi.responses import JSONResponse
from interfaces.json import UserRegister, SuccessResponseJson
from services import UserService

class RegistrationAPI(RouteInterface):
    def __init__(self, session):
        super().__init__()
        self.session = session
        self.router = APIRouter()
        self.setup_routes()
        
        self.service = UserService
        
        
    def setup_routes(self):
        '''
        '''
        @self.router.post("/user", status_code=status.HTTP_201_CREATED, summary="Register user")
        async def AddUser(request: UserRegister, response: Response) -> SuccessResponseJson:
            self.service.user(request)
            response.status_code = status.HTTP_201_CREATED
            return SuccessResponseJson(status=status.HTTP_201_CREATED, message="Your account is created. Please contact admin for activation.")