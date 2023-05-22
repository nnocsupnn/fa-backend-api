from fastapi.responses import JSONResponse
from sqlalchemy.exc import NoResultFound, IntegrityError
from fastapi import status
from fastapi.exceptions import HTTPException

def ex_fa_exception_handler(request, exc: Exception):
    statusRes = status.HTTP_500_INTERNAL_SERVER_ERROR
    if str(exc) == "Invalid credential":
        statusRes = status.HTTP_400_BAD_REQUEST
        
    return JSONResponse(
        status_code=statusRes,
        content={
            "status": statusRes,
            "errorClass": exc.__class__.__name__,
            "message": str(exc)
        }
    )
    

def fa_exception_handler(request, exc: NoResultFound):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "status": 404,
            "errorClass": exc.__class__.__name__,
            "message": str(exc)
        }
    )
    
def fa_exception_handler(request, exc: IntegrityError):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "status": 500,
            "errorClass": exc.__class__.__name__,
            "message": exc._code_str()
        }
    )