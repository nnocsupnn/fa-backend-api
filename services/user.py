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
    LifestyleProtectionInvestments
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
            if user.occupation != None:
                occupation = Occupation(
                    description=user.occupation.description,
                    rank=user.occupation.rank,
                    industry=user.occupation.industry
                )
                
                db.add(occupation)
                db.commit()
            
            userModel = User(
                first_name=user.first_name,
                last_name=user.last_name,
                middle_name=user.middle_name,
                marital=user.marital,
                date_of_birth=user.date_of_birth,
                email_address=user.email_address,
                occupation_id=occupation.id if user.occupation != None else None,
                password=user.password,
                gender=user.gender
            )
            
            db.add(userModel)
            db.commit()
            
            # Populate single data per user
            incomeProtection = IncomeProtection(user_id=userModel.id)
            db.commit()
            incomeProtectionProvision = IncomeProtectionProvision(income_protection_id=incomeProtection.id)
            
            db.add(incomeProtectionProvision)
            
            # Lifestyle
            lifestyle_protection = LifestyleProtection(
                user_id=userModel.id,
                existing_provision=0,
                source_fund=0,
                gov_fund=0,
                other_fund=0
            )
            
            db.add(lifestyle_protection)
            
            if user.user_detail != None:
                userDetail = UserDetail(
                    user_id=userModel.id,
                    year_business=user.user_detail.year_business,
                    retirement_age=user.user_detail.retirement_age,
                    retirement_package=user.user_detail.retirement_package,
                    life_expectancy=user.user_detail.life_expectancy
                )
                
                db.add(userDetail)
            else:
                userDetail = UserDetail(
                    user_id=userModel.id,
                    year_business=1990,
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
            
            propertiesFromJoin = ["marital", "occupation", "user_detail"]
            for field_name, field_type in user.__annotations__.items():
                if field_name in propertiesFromJoin:
                    
                    if field_name == "marital" and user.marital != None:
                        setattr(userModel, field_name, user.marital.value)
                        
                    if field_name == "user_detail" and user.user_detail != None:
                        for deail_field_nae, deail_field_type in user.user_detail.__annotations__.items():
                            if getattr(user.user_detail, deail_field_nae) != None:
                                setattr(userModel.user_detail, deail_field_nae, getattr(user.user_detail, deail_field_nae))
                                
                        
                    if field_name == "occupation" and user.occupation != None:
                        for occ_field_name, occ_field_type in user.occupation.__annotations__.items():
                            if getattr(user.occupation, occ_field_name) != None:
                                setattr(userModel.occupation, occ_field_name, getattr(user.occupation, occ_field_name))
                                
                    
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