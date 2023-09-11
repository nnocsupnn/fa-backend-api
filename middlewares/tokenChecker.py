from fastapi import Request, status
from fastapi.responses import JSONResponse
from models import BlockedSession
from components.db import SessionLocal as Session


async def token_check_middleware(request: Request, call_next):
    path = request.url.path
    method = request.method
    if path.startswith("/fa/api") == False or (path == "/fa/api/user" and method == "POST"):
        response = await call_next(request)
        return response
    else:
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
            raise Exception("Token is blocked. Another session was created.")

        # If the token is not in the blocked token list, proceed with the request
        response = await call_next(request)
        return response
