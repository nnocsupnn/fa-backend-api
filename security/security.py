from fastapi import FastAPI, Depends, status, Request
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException, JWTDecodeError
from fastapi.routing import APIRouter
from fastapi.security import HTTPBearer
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from config.functions import config

security = HTTPBearer()

class Settings(BaseModel):
    authjwt_secret_key: str = config['APP_SECRET']

class AuthSecurity:
    router = APIRouter()
    
    def __init__(self, app: FastAPI):
        self.app = app
        self.initiate()
    
    def initiate(self):
        @AuthJWT.load_config
        def get_config():
            return Settings()

        @self.app.exception_handler(AuthJWTException)
        def authjwt_exception_handler(request, exc):
            return JSONResponse(
                status_code=exc.status_code,
                content={ "status": exc.status_code, "message": exc.message }
            )
        
        '''
        All Required Security header should be added here.
        '''
        @self.app.middleware('http')
        async def security_headers(request: Request, call_next):
            response = await call_next(request)
            response.headers["X-Content-Type-Options"] = "nosniff"
            response.headers["X-Frame-Options"] = "DENY"
            response.headers["Content-Security-Policy"] = "default-src 'self'"
            return response
            
        return self.app

    async def auth_user(security: HTTPBearer = Depends(security), auth: AuthJWT = Depends()):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
        auth_jwt_exception = JWTDecodeError(
            status_code=status.HTTP_401_UNAUTHORIZED,
            message="Invalid authentication credentials"
        )
        
        try:
            auth.jwt_required()
            
            auth.get_raw_jwt()
            current_user = auth.get_raw_jwt()
            
            return current_user["sub"]
        except Exception as e:
            print(e)
            raise auth_jwt_exception
        
    def getApp(self):
        return self.app