from interfaces.route_interface import RouteInterface
from fastapi import APIRouter
from config.db import Base, SessionLocal, engine, User, UserDetail, Occupation, Incomes, IncomeProtection, IncomeProtectionProvision, Dependencies, DependencyDetail, DependencyProvision, Expenses, TextTemplate
import datetime
from interfaces.json import SuccessResponseJson

class TestAPI(RouteInterface):
    def __init__(self, session):
        super().__init__()
        self.session = session
        self.router = APIRouter()
        self.setup_routes()
        
    def setup_routes(self):
        @self.router.get("/populate", summary="Populating test data", description="This route is used for testing only.")
        async def populate() -> SuccessResponseJson:
            with SessionLocal() as db:
                try:
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
                    db.commit()
                    
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
                        password="user12345",
                        date_of_birth=datetime.date(1996, 1, 21),
                        marital="married",
                        active=1, # activate
                        occupation_id=occ.id
                    )
                    
                    db.add(user)
                    db.commit()
                    
                    user_d = UserDetail(
                        user_id=user.id,
                        year_business=2021,
                        retirement_age=65,
                        retirement_package=100000,
                        life_expectancy=90
                    )
                    
                    db.add(user_d)
                    db.commit()
                    
                    income_hist1 = Incomes(
                        user_detail_id=user_d.id,
                        income_amount=85000,
                        description="Income salary",
                        income_started_date=datetime.date(2022, 1, 1),
                        active=1
                    ) 
                    
                    income = Incomes(
                        user_detail_id=user_d.id,
                        income_amount=85000,
                        description="Income salary",
                        income_started_date=datetime.date(2022, 1, 1),
                        active=1
                    )
                    
                    db.add_all([income_hist1, income])
                    
                    expense_tt1_cat = TextTemplate(
                        code="LIFESTYLE",
                        category="expenses_category",
                        description="Lifestyle Expenses"
                    )
                    
                    db.add(expense_tt1_cat)
                    db.commit()
                    '''
                    lifestyle 
                        GUCCI_BAG
                        TUITION
                    '''
                    expense1 = Expenses(
                        user_detail_id=user_d.id,
                        expense_amount=50000,
                        expense_category=expense_tt1_cat.code,
                        description="Tuition ni Junior",
                        expense_started_date=datetime.date(2022, 1, 22),
                        active=1
                    )
                    
                    expense2 = Expenses(
                        user_detail_id=user_d.id,
                        expense_amount=150000,
                        expense_category=expense_tt1_cat.code,
                        description="Gucci wallet",
                        expense_started_date=datetime.date(2022, 1, 22),
                        expense_end_date=datetime.date(2022, 1, 22),
                        active=0
                    )
                    
                    db.add_all([expense1, expense2])
                    
                    
                    
                    dependent1_prov = DependencyProvision(
                        amount=120000
                    )
                    
                    db.add(dependent1_prov)
                    db.commit()
                    
                    dependent1_d = DependencyDetail(
                        dependency_provision_id=dependent1_prov.id,
                        primary_lvl_years=6,
                        secondary_lvl_years=6,
                        tertiary_lvl_years=5,
                        target_entry_age=5,
                        age_before_entry=2,
                        primary_lvl_annual = 10000,
                        secondary_lvl_annual = 20000,
                        tertiary_lvl_annual = 30000,
                        tuition_fee_incr_perc = 6,
                    )
                    
                    db.add(dependent1_d)
                    db.commit()
                    
                    dependent1 = Dependencies(
                        user_id=user.id,
                        dependency_detail_id=dependent1_d.id,
                        name="Naiana Kylie Casupanan",
                        gender="female",
                        relationship="daughter",
                        date_of_birth=datetime.date(2022, 2, 6)
                    )
                    
                    db.add(dependent1)
                    db.commit()
                    
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
                except Exception:
                    db.rollback()
                    db.close()
            
            return SuccessResponseJson(200, "Done")