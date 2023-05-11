from fastapi import APIRouter
from models.User import User
from interfaces.RouteInterface import RouteInterface

class UserAPI(RouteInterface):
    def __init__(self, session):
        super().__init__()
        self.session = session
        self.router = APIRouter()
        self.setup_routes()
    
    def setup_routes(self):
        @self.router.get("/user/{id}")
        async def getUser(id: int):
            if id == None:
                return {
                    "message": "bad request"
                }
            try:
                user = None
                with self.session() as session:
                    user = session.query(User).filter(User.id == id).first()
                    user = user
                    session.close()
                    
                if (user == None):
                    raise Exception("User not found.")
                return user
            except Exception as e:
                return {
                    "error": True,
                    "message": str(e)
                }