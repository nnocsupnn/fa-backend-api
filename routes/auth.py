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
    ACCESS_TOKEN_EXPIRY_MINUTES = 15
    REFRESH_TOKEN_EXPIRY_DAYS = 1
    TOKEN_ALGORITHM = "HS256"

    def __init__(self, session):
        super().__init__()
        self.session = session
        self.router = APIRouter()
        self.setup_routes()
        
    def generate_access_token(self, userId: int, auth: AuthJWT) -> str:
        payload = userId
        access_token = auth.create_access_token(subject=payload, expires_time=timedelta(minutes=self.ACCESS_TOKEN_EXPIRY_MINUTES), algorithm=self.TOKEN_ALGORITHM)
        return access_token

    def generate_refresh_token(self, userId: int, auth: AuthJWT) -> str:
        payload = userId
        refresh_token = auth.create_access_token(subject=payload, expires_time=timedelta(days=self.REFRESH_TOKEN_EXPIRY_DAYS), algorithm=self.TOKEN_ALGORITHM)
        return refresh_token

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
                    
                if user.active == 0:
                    raise Exception(f"User '{user.email_address}' is not activated. Please contact admin.")
                
                if grant_type == "password":
                    expireDelta = timedelta(minutes=15)
                    epochSeconds = (datetime.now() + expireDelta).timestamp()
                    # access_token = auth.create_access_token(subject=user.id, expires_time=expireDelta)
                    access_token = self.generate_access_token(user.id, auth=auth)
                    refresh_token = self.generate_refresh_token(user.id, auth=auth)
                    
                    return JSONResponse(
                        status_code=status.HTTP_201_CREATED,
                        content={ "accessToken": access_token, "refreshToken": refresh_token, "expires": int(epochSeconds) }
                    )
                elif grant_type == "refresh":
                    try:
                        auth.jwt_required()
                        userId = auth.get_jwt_subject()
                        
                        access_token = self.generate_access_token(userId, auth=auth)
                        refresh_token = self.generate_refresh_token(userId, auth=auth)
                        
                        expireDelta = timedelta(minutes=15)
                        epochSeconds = (datetime.now() + expireDelta).timestamp()
                        
                        return JSONResponse(
                            status_code=status.HTTP_201_CREATED,
                            content={ "accessToken": access_token, "refreshToken": refresh_token, "expires": int(epochSeconds) }
                        )
                    except Exception as e:
                        print(str(e))
                        raise Exception("Invalid authentication credentials")
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