import uvicorn
from fastapi import FastAPI, Depends
from config.db import Base, SessionLocal, engine
from config.functions import nullCheckingResponse
from routes import *
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
'''
After creating the routes services, you need to add the API Class here under resource var 
to automatically include in the registered routes
'''
resource = [UserAPI, UserDetailAPI]

'''
Exception routes for auth and other special cases
just to not include the auth module
'''
app.include_router(TestAPI(SessionLocal).router)
app.include_router(AuthAPI(SessionLocal).router)

'''
Run all API Classes to registered to our router
'''
for instance in resource:
    app.include_router(instance(SessionLocal).router, dependencies=[Depends(authSecurity.auth_user)])


# Start Server
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=80, reload=True)