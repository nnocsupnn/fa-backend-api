from models import Dependencies, DependencyDetail, DependencyProvision
from json import loads
from fastapi.exceptions import FastAPIError
from sqlalchemy.orm import joinedload
from sqlalchemy import select
from interfaces.json.api_dtos import User as UserJson, UserRegister, DependencyDetailPostJson, DependencyDetail as DependencyDetailJson
from config.db import SessionLocal as Session

class DependencyDetailService:
    # get all
    def getDependencyDetail(id: int):
        db = Session()
        stmt = select(DependencyDetail).join(Dependencies).where(Dependencies.id == id)
        detail = db.execute(stmt).first()[0]
        # detail = db.query(Dependencies)\
        #     .filter(Dependencies.id == id)\
        #     .first()
            
        return detail
    
    # post
    def save(dependencyId: int, dependecy: DependencyDetailPostJson):
        db = Session()
        dep = db.query(Dependencies).filter(Dependencies.id == dependencyId).first()
        
        depDetail = None
        if dep.dependency_detail_id == None:
            depDetail = DependencyDetail(
                target_entry_age=dependecy.target_entry_age,
                age_before_entry=dependecy.age_before_entry,
                primary_lvl_annual=dependecy.primary_lvl_annual,
                secondary_lvl_annual=dependecy.secondary_lvl_annual,
                tertiary_lvl_annual=dependecy.tertiary_lvl_annual,
                primary_lvl_years=dependecy.primary_lvl_years,
                secondary_lvl_years=dependecy.secondary_lvl_years,
                tertiary_lvl_years=dependecy.tertiary_lvl_years,
                tuition_fee_incr_perc=dependecy.tuition_fee_incr_perc
            )
            
            db.add(depDetail)
            db.commit()
            
            setattr(dep, "dependency_detail_id", depDetail.id)
        else:
            raise Exception("DependencyDetail already has content.")

        
        if getattr(dependecy, "dependency_provision") != None and depDetail.dependency_provision == None:
            depProvision = DependencyProvision(
                amount=dependecy.dependency_provision.amount
            )
            
            db.add(depProvision)
            db.commit()
            
            setattr(depDetail, "dependency_provision_id", depProvision.id)
            
        db.commit()
        db.refresh(dep)
        db.close()
        
        return dep

    # patch
    def updateDependency(id: int, request: DependencyDetailJson):
        result = None
        with Session() as db:
            # dep = dependency.dependency_detail
            stmt = select(DependencyDetail).join(Dependencies).where(Dependencies.id == id)
            dep = db.execute(stmt).first()[0]
            
            if dep == None:
                raise Exception("DependencyDetail not exists.")
            
            for field_name, field_type in request.__annotations__.items():
                if getattr(request, field_name) != None and field_name != "dependency_provision":
                    setattr(dep, field_name, getattr(request, field_name))
                    
                if field_name == "dependency_provision" and getattr(request, field_name) != None:
                    if dep.dependency_provision_id != None:
                        for dep_prov_name, dep_prov_type in request.dependency_provision.__annotations__.items():
                            setattr(dep.dependency_provision, dep_prov_name, getattr(request.dependency_provision, dep_prov_name))
                    else:
                        dep_prov = DependencyProvision(amount=request.dependency_provision.amount)
                        db.add(dep_prov)
                        db.commit()
                        setattr(dep.dependency_provision_id, "dependency_provision_id", dep_prov.id)
                    
            db.commit()
            result = db.query(DependencyDetail).filter(DependencyDetail.id == dep.id).first()
            db.refresh(dep)
            db.close()
        
        return result