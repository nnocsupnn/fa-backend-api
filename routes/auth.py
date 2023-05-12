from fastapi import APIRouter, Response, Depends, status
from fastapi.exceptions import FastAPIError
from models import User
from sqlalchemy.orm import joinedload
from interfaces.route_interface import RouteInterface
from interfaces.json.api_dtos import AuthenticationJson
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from datetime import timedelta, datetime

'''
'''
class AuthAPI(RouteInterface):
    def __init__(self, session):
        super().__init__()
        self.session = session
        self.router = APIRouter()
        self.setup_routes()
        
    
    def setup_routes(self):
        @self.router.post("/jwt/auth")
        async def login(credential: AuthenticationJson, response: Response, auth: AuthJWT = Depends()) -> JSONResponse:
            try:
                payload = credential.json()
                
                # Credential
                email = getattr(credential, "username")
                password = getattr(credential, "password")
                grant_type = getattr(credential, "grant_type")
                
                # Getting User
                user = None
                with self.session() as db:
                    user = db.query(User).filter(User.email_address == email).first()
                    db.close()
                
                # Validations
                if user != None and not user.check_password(password=password) or user == None:
                    raise Exception("Invalid credential")
                    
                if grant_type == "password":
                    expireDelta = timedelta(minutes=15)
                    epochSeconds = (datetime.now() + expireDelta).timestamp()
                    access_token = auth.create_access_token(subject=payload, expires_time=expireDelta)
                    
                    return JSONResponse(
                        status_code=status.HTTP_201_CREATED,
                        content={ "accessToken": access_token, "expires": int(epochSeconds) }
                    )
                else:
                    raise Exception("Invalid grant_type")
            except Exception as e:
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={
                        "status": status.HTTP_401_UNAUTHORIZED,
                        "message": str(e)
                    }
                )