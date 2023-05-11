from fastapi import FastAPI
import uvicorn
import datetime

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
    with SessionLocal() as db:
        rank = TextTemplate(
            code="IT_VP",
            category="rank",
            description="Vice President"
        )
        
        industry = TextTemplate(
            code="IT",
            category="industry",
            description="Information Technology"
        )
        
        db.add_all([rank, industry])
        
        occ = Occupation(
            description="VPIT",
            rank=rank.code,
            industry=industry.code
        )
        
        db.add(occ)
        db.commit()
        
        user = User(
            first_name="Nino",
            last_name="Casupanan",
            email_address="nnocsupnn@gmail.com",
            date_of_birth=datetime.date(1996, 1, 21),
            marital="married",
            occupation_id=occ.id
        )
        
        db.add(user)
        db.commit()
        
        user_d = UserDetails(
            user_id=user.id,
            year_business=2021,
            retirement_age=65,
            retirement_package=100000,
            life_expectancy=90
        )
        
        db.add(user_d)
        db.commit()
        
        income_tt = TextTemplate(
            code="SALARY",
            category="income",
            description="Salary"
        )
        
        db.add(income_tt)
        db.commit()
        
        income_hist1 = Income(
            user_detail_id=user_d.id,
            income_amount=85000,
            income_type=income_tt.id,
            description="Income salary",
            income_started_date=datetime.date(2022, 1, 1),
            active=1
        ) 
        
        income = Income(
            user_detail_id=user_d.id,
            income_amount=85000,
            income_type=income_tt.id,
            description="Income salary",
            income_started_date=datetime.date(2022, 1, 1),
            active=1
        )
        
        db.add_all([income_hist1, income])
        
        expense_tt1 = TextTemplate(
            code="TUITION",
            category="expenses",
            description="Tuition"
        )
        
        expense_tt2 = TextTemplate(
            code="GUCCI_BAG",
            category="expenses",
            description="Gucci Bag"
        )
        
        db.add_all([expense_tt1, expense_tt2])
        db.commit()
        
        expense1 = Expenses(
            user_detail_id=user_d.id,
            expense_amount=50000,
            expense_type=expense_tt1.id,
            description="Tuition ni Junior",
            expense_started_date=datetime.date(2022, 1, 22),
            active=1
        )
        
        expense2 = Expenses(
            user_detail_id=user_d.id,
            expense_amount=150000,
            expense_type=expense_tt2.id,
            description="Gucci wallet",
            expense_started_date=datetime.date(2022, 1, 22),
            expense_end_date=datetime.date(2022, 1, 22),
            active=0
        )
        
        db.add_all([expense1, expense2])
        
        dependent1 = Dependencies(
            user_id=user.id,
            name="Naiana Kylie Casupanan",
            gender="female",
            relationship="daughter",
            date_of_birth=datetime.date(2022, 2, 6)
        )
        
        db.add(dependent1)
        db.commit()
        
        dependent1_d = DependencyDetail(
            dependency_id=dependent1.id,
            type="",
            target_years=2024,
            target_entry_age=5,
            age_before_entry=2,
            amount=10000
        )
        
        db.add(dependent1_d)
        
        dependent1_prov = DependencyProvision(
            user_id=user.id,
            amount=10000
        )
        
        db.add(dependent1_prov)
        
        # Income Pro
        income_pro = IncomeProtection(
            user_id=user.id,
            income_amount=125000,
            date_started=datetime.date(2021, 2, 22)
        )
        
        db.add(income_pro)
        db.commit()
        
        income_pro_prov = IncomeProtectionProvision(
            income_protection_id=income_pro.id,
            amount=10000
        )
        
        db.add(income_pro_prov)
        
        db.commit()
        db.close()
    
    return { "status": 200, "message": "Done" }

# Start Server
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)