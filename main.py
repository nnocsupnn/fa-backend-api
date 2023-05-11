from fastapi import FastAPI
import uvicorn

from components.db import Base, SessionLocal, engine, User, UserDetails, Occupation, Income, IncomeProtection, IncomeProtectionProvision, Dependencies, DependencyDetail, DependencyProvision, Expenses, TextTemplate
from components.functions import nullCheckingResponse
from routes import UserAPI

# Intialize db (DDL)
Base.metadata.create_all(engine, checkfirst=True)

app = FastAPI()

# # # # # # # #
#  Routes     #
# # # # # # # #
app.include_router(UserAPI(SessionLocal).router)

@app.get("/populate")
def populateData():
    user = User(
        first_name=""
    )
    return { "status": 200, "message": "Done" }

# Start Server
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)