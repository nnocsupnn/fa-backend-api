import uvicorn
from fastapi.responses import RedirectResponse
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Depends
from sqlalchemy.exc import IntegrityError, NoResultFound
from config.db import Base, SessionLocal, engine
from config.functions import nullCheckingResponse
from config.exception_handlers import fa_exception_handler, ex_fa_exception_handler
from routes import *
from security.jwt_auth import AuthSecurity

# Intialize db (DDL)
Base.metadata.create_all(engine, checkfirst=True)
    
app = FastAPI(
    title="Financial Analysis API",
    description="This docs is for financial analysis application.",
    redoc_url="/api/docs"
)

'''
CORS
'''
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST", "DELETE", "PATCH", "PUT"],
    allow_headers=["*"]
)
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
resource = [
    UserAPI, 
    UserDetailAPI, 
    TextTemplateAPI, 
    DepdenciesAPI, 
    DepdencyDetailAPI,
    IncomeAPI,
    ExpensesAPI,
    IncomeProtectionAPI,
    LifestyleProtectionAPI,
    WealthAPI
]

'''
Exception routes for auth and other special cases
just to not include the auth module
'''
app.include_router(TestAPI(SessionLocal).router, tags=["maintenance"])
app.include_router(AuthAPI(SessionLocal).router, tags=["AuthenticationAPI"])


'''
Run all API Classes to registered to our router
'''
for instance in resource:
    app.add_exception_handler(Exception, ex_fa_exception_handler)
    app.add_exception_handler(NoResultFound, fa_exception_handler)
    app.add_exception_handler(IntegrityError, fa_exception_handler)
    
    app.include_router(instance(SessionLocal).router, dependencies=[Depends(authSecurity.auth_user)], prefix="/fa/api", tags=[instance.__name__])


# Start Server
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=80, reload=True)