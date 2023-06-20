from fastapi import Request, status
from fastapi.responses import JSONResponse
from models import BlockedSession
from components.db import SessionLocal as Session



async def token_check_middleware(request: Request, call_next):
    if request.url.path.startswith("/fa/api") == False:
        response = await call_next(request)
        return response
    
    blocked_token_list = []
    with Session() as db:
        tokens = db.query(BlockedSession).all()
        for token in tokens:
            blocked_token_list.append(token.token)
        db.close()
        
    # Get the token from the request headers
    reqToken = request.headers.get("Authorization")
    
    # Check if the token is in the blocked token list
    if reqToken.split(" ")[1] in blocked_token_list:
        raise Exception("TOKEN_INVALID")

    # If the token is not in the blocked token list, proceed with the request
    response = await call_next(request)
    return response
