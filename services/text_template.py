from models import TextTemplate as TT
from json import loads
from config.functions import make_code_string
from fastapi.exceptions import FastAPIError
from sqlalchemy import exists
from fastapi.logger import logger
from interfaces.json.api_dtos import TextTemplate
from config.db import SessionLocal as Session

class TextTemplateService:
    def prepopulateTemplates():
        # TODO: Prepopulate templates
        ranks = [
            "IT Technician",
            "Help Desk/Support Analyst",
            "Network Support Specialist",
            "Data Entry Operator",
            "Hardware Technician",
            "Application Support Analyst",
            "Systems Administrator",
            "Network Administrator",
            "Database Administrator",
            "Security Analyst/Engineer",
            "Software Developer/Engineer",
            "Business Analyst",
            "IT Project Manager",
            "IT Manager",
            "IT Director",
            "Chief Technology Officer (CTO)",
            "Chief Information Officer (CIO)"
        ]
        
        industries = [
            "Information Technology",
            "Farming",
            "Health Care",
            "Insurance"
        ]
        
        expenses_categories = [
            "Essentials",
            "Business",
            "Optional",
            "Educational Expense",
            "Amortizations"
        ]
        
        with Session() as db:
            try:
                insert = []
                # Ranks
                for rank in ranks:
                    rankq = db.query(exists().where(TT.description == rank))
                    rank_exists = db.execute(rankq).scalar()

                    if not rank_exists:
                        i = TT(
                            code=make_code_string(rank),
                            description=rank,
                            category="rank"
                        )
                        
                        insert.append(i)
                
                # Industries
                for industry in industries:
                    industryq = db.query(exists().where(TT.description == industry))
                    industry_exists = db.execute(industryq).scalar()

                    if not industry_exists:
                        i = TT(
                            code=make_code_string(industry),
                            description=industry,
                            category="industry"
                        )
                        
                        insert.append(i)
                # Expenses
                for expenses_category in expenses_categories:
                    expenses_categoryq = db.query(exists().where(TT.description == expenses_category))
                    expenses_category_exists = db.execute(expenses_categoryq).scalar()

                    if not expenses_category_exists:
                        i = TT(
                            code=make_code_string(expenses_category),
                            description=expenses_category,
                            category="expenses_category"
                        )
                        
                        insert.append(i)
                
                db.add_all(insert)
                        
                db.commit()
                db.close()
                
                print("--- Prepopulating templates completed.")
            except Exception:
                db.rollback()
                
        return True
    
    def templates():
        return TT.getTemplates()
    
    def templatesByCategory(category: str):
        return TT.getTemplatesByCategory(category)

    def template(subj: str):
        return TT.getTemplate(subj=subj)
    
    def save(subj: TextTemplate):
        result = None
        db = Session()
        
        tt = TT(
            description=subj.description,
            category=subj.category
        )
        
        db.add(tt)
        db.commit()
        
        tt.code = make_code_string(subj.description) + "_" + str(tt.id)
        
        db.commit()
        result = db.query(TT).filter(TT.id == tt.id).first()
        db.close()
        
        return result
        
    def delete(code: str):
        db = Session()
        
        try:
            result = db.query(TT).where(TT.code == code).first()
            if result != None:
                db.query(TT).where(TT.code == code).delete()
                db.commit()
            
            db.close()
            return result
        except Exception as e:
            db.close()
            raise e
            