from fastapi import FastAPI, Depends
import uvicorn
import datetime
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException

from components.db import Base, SessionLocal, engine, User, UserDetail, Occupation, Incomes, IncomeProtection, IncomeProtectionProvision, Dependencies, DependencyDetail, DependencyProvision, Expenses, TextTemplate
from components.functions import nullCheckingResponse
from routes import UserAPI, AuthAPI, TestAPI, UserDetailAPI
from security.jwt_auth import AuthSecurity

# Intialize db (DDL)
Base.metadata.create_all(engine, checkfirst=True)

app = FastAPI()

'''
Security Implementation
'''
authSecurity = AuthSecurity(app=app)
app = authSecurity.getApp()

# # # # # # # #
#  Routes     #
# # # # # # # #

app.include_router(TestAPI(SessionLocal).router)
app.include_router(AuthAPI(SessionLocal).router)
app.include_router(UserAPI(SessionLocal).router, dependencies=[Depends(authSecurity.auth_user)])
app.include_router(UserDetailAPI(SessionLocal).router, dependencies=[Depends(authSecurity.auth_user)])

# Start Server
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=80, reload=True)