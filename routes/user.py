from fastapi import APIRouter, Response, status
from fastapi.exceptions import FastAPIError
from models import User
from json import loads as jsonResponse
from sqlalchemy.orm import joinedload
from interfaces.RouteInterface import RouteInterface
from interfaces.json.user import User as UserJson, Occupation

'''
UserAPI is class for User Resource

@interface RouteInterface
@author Nino Casupanan
@memberof MediCard
'''
class UserAPI(RouteInterface):
    def __init__(self, session):
        super().__init__()
        self.session = session
        self.router = APIRouter()
        self.setup_routes()
    
    def setup_routes(self):
        @self.router.get("/user/{id}")
        async def getUser(id: int, response: Response):
            if id == None:
                return {
                    "message": "bad request"
                }
            try:
                user = User.get_user(id)
                    
                if (user == None):
                    raise Exception("User not found.")
                
                return user
            except Exception as e:
                response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
                return {
                    "message": str(e)
                }
                
        @self.router.post("/user", status_code=status.HTTP_201_CREATED)
        async def user(request: UserJson, response: Response):
            try:
                data = request.json()
                
                # Process data below
                print(data)
                # with self.session() as session:
                #     session.add()
                # End Process
                
                return jsonResponse(data)
            except FastAPIError as e:
                response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
                return {
                    "message": str(e)
                }
            except Exception as e:
                response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
                return {
                    "message": str(e)
                }
            