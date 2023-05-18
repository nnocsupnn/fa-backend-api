from models import User, Occupation, UserDetail
from json import loads
from fastapi.exceptions import FastAPIError

from interfaces.json.api_dtos import User as UserJson, UserRegister
from config.db import SessionLocal as Session

class UserService:
    
    def getUser(id: int):
        try:
            user = User.get_user(id)
            if (user == None):
                raise Exception("User not found.")
            return user
        except Exception as e:
            raise e
    
    
    def user(user: UserRegister):
        # Process data below
        with Session() as db:
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
                occupation_id=occupation.id,
                password=user.password
            )
            
            db.add(userModel)
            db.commit()
            
            if user.user_detail != None:
                userDetail = UserDetail(
                    user_id=userModel.id,
                    year_business=user.user_detail.year_business,
                    retirement_age=user.user_detail.retirement_age,
                    retirement_package=user.user_detail.retirement_package,
                    life_expectancy=user.user_detail.life_expectancy
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
                        userModel.marital = user.marital.value
                        
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