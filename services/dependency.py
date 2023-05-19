from models import User, Dependencies
from json import loads
from fastapi.exceptions import FastAPIError

from interfaces.json.api_dtos import User as UserJson, UserRegister, Dependencies as DependenciesJson
from config.db import SessionLocal as Session

class DependencyService:
    # get all
    def getDependencies(id: int):
        db = Session()
        dependencies = db.query(Dependencies).where(Dependencies.user_id == id).all()
        return dependencies
    
    # post
    def dependency(id: int, dependecy: DependenciesJson):
        dep = Dependencies(
            user_id=id,
            name=dependecy.name,
            gender=dependecy.gender,
            relationship=dependecy.relationship,
            date_of_birth=dependecy.date_of_birth
        )
        
        with Session() as db:
            db.add(dep)
            db.commit()
            db.refresh(dep)
            db.close()
            
        return dep

    # patch
    def updateDependency(id: int, request: DependenciesJson):
        db = Session()
        dep = db.query(Dependencies).filter(Dependencies.id == id).first()
        
        if dep == None:
            raise Exception("Dependency not exists.")
        
        for field_name, field_type in request.__annotations__.items():
            print(getattr(request, field_name))
            if getattr(request, field_name) != None:
                setattr(dep, field_name, getattr(request, field_name))
                
        db.commit()
        db.refresh(dep)
        db.close()
        
        return dep