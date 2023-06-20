from fastapi import APIRouter, Response, Depends, status
from models import User, LoginSession, BlockedSession
from interfaces.route_interface import RouteInterface
from interfaces.json import AuthenticationJson, JwtResponseJson, GeneratedTokenPayload, SuccessResponseJson
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
        
    def validateUserSession(self, userId, tokenExpr: int):
        session = None
        with self.session() as db:
            session = db.query(LoginSession).filter(LoginSession.user_id == userId).first()
            # If requesting is from logout
            if session != None and tokenExpr == 0:
                db.query(LoginSession).filter(LoginSession.user_id == userId).delete()
                db.commit()
            else:
                if tokenExpr == 0:
                    raise Exception("User already logged out or not logged in.")
                if session == None:
                    session = LoginSession(user_id=userId, token_expr=tokenExpr)
                    db.add(session)
                    db.commit()
                else:
                    if session.isTokenExpired():
                        session = LoginSession(user_id=userId, token_expr=tokenExpr)
                        db.add(session)
                        db.commit()
                    else:
                        db.close()
                        raise Exception("You are currently logged in to other session.")
                
            db.close()
            
        pass
        
    def generate_access_token(self, userId: int, auth: AuthJWT) -> GeneratedTokenPayload:
        payload = userId
        expires = timedelta(days=self.ACCESS_TOKEN_EXPIRY_DAYS)
        access_token = auth.create_access_token(subject=payload, expires_time=expires, algorithm=self.TOKEN_ALGORITHM)
        return GeneratedTokenPayload(token=access_token, expires=(datetime.now() + expires).timestamp())

    def generate_refresh_token(self, userId: int, auth: AuthJWT) -> GeneratedTokenPayload:
        payload = userId
        expires = timedelta(days=self.REFRESH_TOKEN_EXPIRY_DAYS)
        refresh_token = auth.create_refresh_token(subject=payload, expires_time=expires, algorithm=self.TOKEN_ALGORITHM)
        return GeneratedTokenPayload(token=refresh_token, expires=(datetime.now() + expires).timestamp())

    def setup_routes(self):
        @self.router.post("/jwt/auth", summary="Get JWT Auth", description="Credentials are from your email and registered password.\nFor `refresh token`. Please see the readme instructions.", status_code=status.HTTP_201_CREATED, response_description="Successfully logged in.")
        async def login(credential: AuthenticationJson, response: Response, auth: AuthJWT = Depends()) -> JwtResponseJson:
            payload = credential.json()
                
            # Credential
            email = getattr(credential, "username")
            password = getattr(credential, "password")
            grant_type = getattr(credential, "grant_type")
            
            # Getting User
            user = None
            if grant_type == "password":
                with self.session() as db:
                    user = db.query(User).filter(User.email_address == email).first()
                    db.close()
                    
                # Validations
                if user != None and not user.check_password(password=password) or user == None:
                    raise Exception("Invalid credential")
                    
                if user.active == 0:
                    raise Exception(f"User '{user.email_address}' is not activated. Please contact admin.")
                
                # access_token = auth.create_access_token(subject=user.id, expires_time=expireDelta)
                aToken = self.generate_access_token(user.id, auth=auth)
                rToken = self.generate_refresh_token(user.id, auth=auth)
                
                token = JwtResponseJson(
                    accessToken=aToken.token,
                    refreshToken=rToken.token,
                    expires=int(aToken.expires),
                    refreshTokenExpires=int(rToken.expires),
                    is_first_time_login=user.is_first_time_login
                )
                
                self.validateUserSession(user.id, aToken.expires)
                
                response.status_code = status.HTTP_201_CREATED
                return token
            elif grant_type == "refresh":
                try:
                    auth.jwt_refresh_token_required()
                    userId = auth.get_jwt_subject()
                    
                    with self.session() as db:
                        user = db.query(User).filter(User.id == userId).first()
                        db.close()
                        
                    aToken = self.generate_access_token(userId, auth=auth)
                    rToken = self.generate_refresh_token(userId, auth=auth)
                    
                    token = JwtResponseJson(
                        accessToken=aToken.token,
                        refreshToken=rToken.token,
                        expires=int(aToken.expires),
                        refreshTokenExpires=int(rToken.expires),
                        is_first_time_login=user.is_first_time_login
                    )
                    
                    self.validateUserSession(userId, aToken.expires)
                    
                    response.status_code = status.HTTP_201_CREATED
                    return token
                except Exception as e:
                    # print(str(e))
                    raise Exception("Invalid authentication credentials")
            else:
                raise Exception("Invalid grant_type")
            
        @self.router.post("/logout", summary="Logout User", description="Logout current user session. `token` is required.")
        async def logout(response: Response, auth: AuthJWT = Depends()) -> SuccessResponseJson:
            auth.jwt_required()
            userId = auth.get_jwt_subject()
            
            token = auth._token
            with self.session() as db:
                session = db.query(BlockedSession).filter(BlockedSession.token == token).first()
                if session != None:
                    raise Exception("Your session is invalid.")
                else:
                    session = BlockedSession(token=token)
                    db.add(session)
                    db.commit()
                db.close()
                
            self.validateUserSession(userId, 0)
                
            response.status_code = status.HTTP_200_OK
            return SuccessResponseJson(status=200, message="Succesfully logged out.")