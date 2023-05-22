from fastapi import APIRouter, Response, Depends, status
from models import User
from interfaces.route_interface import RouteInterface
from interfaces.json import AuthenticationJson, JwtResponseJson
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from datetime import timedelta, datetime

'''
'''
class AuthAPI(RouteInterface):
    ACCESS_TOKEN_EXPIRY_DAYS = 1
    REFRESH_TOKEN_EXPIRY_DAYS = 7
    TOKEN_ALGORITHM = "HS256"

    def __init__(self, session):
        super().__init__()
        self.session = session
        self.router = APIRouter()
        self.setup_routes()
        
    def generate_access_token(self, userId: int, auth: AuthJWT) -> str:
        payload = userId
        access_token = auth.create_access_token(subject=payload, expires_time=timedelta(days=self.ACCESS_TOKEN_EXPIRY_DAYS), algorithm=self.TOKEN_ALGORITHM)
        return access_token

    def generate_refresh_token(self, userId: int, auth: AuthJWT) -> str:
        payload = userId
        refresh_token = auth.create_access_token(subject=payload, expires_time=timedelta(days=self.REFRESH_TOKEN_EXPIRY_DAYS), algorithm=self.TOKEN_ALGORITHM)
        return refresh_token

    def setup_routes(self):
        @self.router.post("/jwt/auth", summary="Get JWT Auth", description="Credentials are from your email and registered password.", status_code=status.HTTP_201_CREATED, response_description="Successfully logged in.")
        async def login(credential: AuthenticationJson, response: Response, auth: AuthJWT = Depends()) -> JwtResponseJson:
            payload = credential.json()
                
            # Credential
            email = getattr(credential, "username")
            password = getattr(credential, "password")
            grant_type = getattr(credential, "grant_type")
            
            if grant_type == "password":
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
                
                expireDelta = timedelta(minutes=15)
                epochSeconds = (datetime.now() + expireDelta).timestamp()
                # access_token = auth.create_access_token(subject=user.id, expires_time=expireDelta)
                access_token = self.generate_access_token(user.id, auth=auth)
                refresh_token = self.generate_refresh_token(user.id, auth=auth)
                
                token = JwtResponseJson(
                    accessToken=access_token,
                    refreshToken=refresh_token,
                    expires=int(epochSeconds)
                )
                
                response.status_code = status.HTTP_201_CREATED
                return token
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