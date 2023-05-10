from fastapi import FastAPI
import uvicorn

from components.db import Base, SessionLocal, engine, User, Occupation
from components.functions import nullCheckingResponse

# Intialize db (DDL)
Base.metadata.create_all(engine, checkfirst=True)

app = FastAPI()

@app.get("/user/{id}")
def user(id: int):
    user = None
    with SessionLocal() as session:
        user = session.query(User).filter(User.id == id).first()
        user = user.occupation
        session.close()
    return user

@app.get("/user/{id}/details")
def details(id: int):
    user = User.get_user_details(id)
    return nullCheckingResponse(user)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

# python -m uvicorn main:app --reload