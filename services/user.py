from models import User, \
    Occupation, \
    UserDetail, \
    Incomes, \
    Expenses, \
    Dependencies, \
    DependencyDetail, \
    DependencyProvision, \
    IncomeProtection, \
    IncomeProtectionProvision, \
    LifestyleProtection, \
    LifestyleProtectionInvestments, \
    Wealth, \
    Kapritso
from json import loads
from fastapi.exceptions import FastAPIError

from interfaces.json.api_dtos import User as UserJson, UserRegister
from config.db import SessionLocal as Session
from sqlalchemy.exc import NoResultFound

class UserService:
    
    def getUser(id: int):
        try:
            user = User.get_user(id)
            if (user == None):
                raise NoResultFound("User not found.")
            return user
        except Exception as e:
            raise e
    
    
    def user(user: UserRegister):
        # Process data below
        with Session() as db:
            userModel = User(
                first_name=user.first_name,
                last_name=user.last_name,
                middle_name=user.middle_name,
                marital=user.marital,
                date_of_birth=user.date_of_birth,
                email_address=user.email_address,
                password=user.password,
                gender=user.gender
            )
            
            db.add(userModel)
            db.commit()
            
            if user.occupation != None:
                occupation = Occupation(
                    user_id=userModel.id,
                    description=user.occupation.description if user.occupation.rank != None else None,
                    rank=user.occupation.rank if user.occupation.rank != None else None,
                    industry=user.occupation.industry if user.occupation.industry != None else None
                )
                
                db.add(occupation)
            
            # Populate single data per user
            incomeProtection = IncomeProtection(user_id=userModel.id)
            db.add(incomeProtection)
            db.commit()
            
            incomeProtectionProvision = IncomeProtectionProvision(income_protection_id=incomeProtection.id)
            
            db.add(incomeProtectionProvision)
            
            # Lifestyle
            lifestyle_protection = LifestyleProtection(
                user_id=userModel.id,
                existing_provision=0,
                source_fund=0,
                gov_fund=0,
                other_fund=0,
                projection_rate=0
            )
            
            db.add(lifestyle_protection)
            
            wealth = Wealth(
                user_id=userModel.id,
                real_properties_value = 0,
                personal_properties_value = 0,
                liquid_investments_value = 0,
                projected_apprec_rate_per_year = 2,
                projected_rate_return_on_fixed = 5,
                tax_rate = 1
            )
            
            db.add(wealth)
            
            kapritso = Kapritso(
                user_id = userModel.id,
                factor = 7,
                daily_cost = 100
            )
            
            db.add(kapritso)
            
            if user.user_detail != None:
                userDetail = UserDetail(
                    user_id=userModel.id,
                    year_business=user.user_detail.year_business if user.user_detail.year_business != None else 0,
                    retirement_age=user.user_detail.retirement_age if user.user_detail.retirement_age != None else 0,
                    retirement_package=user.user_detail.retirement_package if user.user_detail.retirement_package != None else 0,
                    life_expectancy=user.user_detail.life_expectancy if user.user_detail.life_expectancy != None else 0,
                    avg_annual_salary_incr=user.user_detail.avg_annual_salary_incr if user.user_detail.avg_annual_salary_incr != None else 0
                )
                
                db.add(userDetail)
            else:
                userDetail = UserDetail(
                    user_id=userModel.id,
                    year_business=0,
                    retirement_age=65,
                    retirement_package=0,
                    life_expectancy=0
                )
                
                db.add(userDetail)
                
            db.commit()
            db.close()
            
        return True
        
    def updateUser(id, user: UserJson):
        userModel = None
        with Session() as db:
            userModel = db.query(User).filter(User.id == id).first()
            
            if userModel == None:
                db.close()
                raise NoResultFound(f"User with ID ({id}) not found.")
            
            propertiesFromJoin = ["marital", "occupation", "user_detail"]
            for field_name, field_type in user.__annotations__.items():
                if field_name in propertiesFromJoin:
                    
                    if field_name == "marital" and user.marital != None:
                        setattr(userModel, field_name, user.marital.value)
                        
                    if field_name == "user_detail" and user.user_detail != None:
                        for deail_field_nae, deail_field_type in user.user_detail.__annotations__.items():
                            if getattr(user.user_detail, deail_field_nae) != None:
                                setattr(userModel.user_detail, deail_field_nae, getattr(user.user_detail, deail_field_nae))
                                
                    if field_name == "occupation" and user.occupation != None and userModel.occupation != None:
                        for occ_field_name, occ_field_type in user.occupation.__annotations__.items():
                            if getattr(user.occupation, occ_field_name) != None:        
                                setattr(userModel.occupation, occ_field_name, getattr(user.occupation, occ_field_name))
                    else:
                        if user.occupation != None and userModel.occupation == None:
                            occ = Occupation(
                                user_id=userModel.id,
                                rank=user.occupation.rank,
                                industry=user.occupation.industry
                            )
                            
                            db.add(occ)
                            db.commit()
                        # for occ_field_name, occ_field_type in user.occupation.__annotations__.items():
                        #     if getattr(user.occupation, occ_field_name) != None:
                        #         setattr(userModel.occupation, occ_field_name, getattr(user.occupation, occ_field_name))
                    
                    continue
                else:
                    if getattr(user, field_name) != None:
                        setattr(userModel, field_name, getattr(user, field_name))
                
            db.commit()
            db.refresh(userModel)
            db.close()
            
        
        return userModel
    
    def deleteUser(id: int):
        try:
            with Session() as db:
                dependencies = db.query(Dependencies).filter(Dependencies.user_id == id).first()
                dependencDetail = db.query(DependencyDetail).filter(DependencyDetail.id == dependencies.dependency_detail_id).first()
                
                db.query(Dependencies).where(Dependencies.user_id == id).delete()
                db.query(DependencyDetail).where(DependencyDetail.id == dependencies.dependency_detail_id).delete()
                db.query(DependencyProvision).where(DependencyProvision.id == dependencDetail.dependency_provision_id).delete()
                
                incomeProtec = db.query(IncomeProtection).filter(IncomeProtection.user_id == id).first()
                
                db.query(IncomeProtectionProvision).where(IncomeProtectionProvision.income_protection_id == incomeProtec.id).delete()
                db.query(IncomeProtection).where(IncomeProtection.user_id == id).delete()
                
                
                db.query(Incomes).where(Incomes.user_detail_id == id).delete()
                db.query(Expenses).where(Expenses.user_detail_id == id).delete()
                db.query(UserDetail).where(UserDetail.user_id == id).delete()
                db.query(User).where(User.id == id).delete()
                db.commit()
                db.close()
                
            return True
        except Exception as e:
            raise e