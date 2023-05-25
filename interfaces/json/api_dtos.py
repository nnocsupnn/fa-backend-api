from pydantic import BaseModel, Field
from datetime import date
from enum import Enum
from typing import Optional, List

'''
Enums
'''
class UserLevel(str, Enum):
    admin = "admin"
    user = "user"
class Gender(str, Enum):
    female = "female"
    male = "male"
    
class Relationship(str, Enum):
    son = "son"
    daughter = "daughter"
    mother = "mother"
    father = "father"
    grand_mother = "grand_mother"
    grand_father = "grand_father"
    sister = "sister"
    brother = "brother"
    wife = "wife"
    
class Marital(str, Enum):
    single = "single"
    married = "married"
    divorced = "divorced"
    separated = "separated"
    widowed = "widowed"

class TextTemplateCategory(str, Enum):
    expenses = "expenses"
    education = "education"
    rank = "rank"
    industry = "industry"
    expenses_category = "expenses_category"
'''
Models
'''

class DependencyProvision(BaseModel):
    amount: float
    
class DependencyDetail(BaseModel):
    target_entry_age: Optional[int] = None
    age_before_entry: Optional[int] = None
    primary_lvl_annual: Optional[float] = None
    secondary_lvl_annual: Optional[float] = None
    tertiary_lvl_annual: Optional[float] = None
    primary_lvl_years: Optional[int] = None
    secondary_lvll_years: Optional[int] = None
    tertiary_lvll_years: Optional[int] = None
    tuition_fee_incr_perc: Optional[float] = None
    dependency_provision: Optional[DependencyProvision] = None
    
class DependencyDetailPostJson(BaseModel):
    target_entry_age: int
    age_before_entry: int
    primary_lvl_annual: float
    secondary_lvl_annual: float
    tertiary_lvl_annual: float
    primary_lvl_years: int
    secondary_lvl_years: int
    tertiary_lvl_years: int
    tuition_fee_incr_perc: int
    dependency_provision: Optional[DependencyProvision] = None

    
class Expenses(BaseModel):
    user_detail_id: int
    expense_amount: float
    description: str
    expense_started_date: date
    expense_end_date: date
    

    
class Income(BaseModel):
    user_detail_id: int
    income_amount: float
    description: str
    income_started_date: date
    income_end_date: date

class IncomeProtection(BaseModel):
    user_id: int
    income_amount: float
    date_started: date
    
class IncomeProtectionProvision(BaseModel):
    income_protection_id: int
    amount: float
    date_started: date
    
class TextTemplate(BaseModel):
    description: str
    category: TextTemplateCategory
    
class Occupation(BaseModel):
    description: Optional[str] = None
    rank: Optional[str] = None
    industry: Optional[str] = None

class UserDetail(BaseModel):
    year_business: Optional[int] = None
    retirement_age: Optional[int] = None
    retirement_package: Optional[float] = None
    life_expectancy: Optional[int] = None
    avg_annual_salary_incr: Optional[float] = Field(description="Average Annual Salary Increase", default=None)
    max_age_of_dependent: Optional[int] = Field(description="Maximum Age of Dependency", default=None)
    min_age_of_dependent: Optional[int] = Field(description="Age of Youngest Dependent", default=None)
    
    
class UserRegister(BaseModel):
    first_name: str
    middle_name: Optional[str] = None
    last_name: str
    email_address: str
    date_of_birth: date
    marital: Optional[Marital] = None
    occupation: Optional[Occupation] = None
    user_detail: Optional[UserDetail] = None
    gender: Gender
    password: str = Field(alias="password", min_length=8, regex=r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]+$")
    
class User(BaseModel):
    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    last_name: Optional[str] = None
    email_address: Optional[str] = None
    date_of_birth: Optional[date] = None
    marital: Optional[Marital] = None
    occupation: Optional[Occupation] = None
    user_detail: Optional[UserDetail] = None
    user_level: Optional[str] = None
    active: Optional[int] = None
    basic_salary: Optional[float] = None
    net_salary: Optional[float] = None
    
class Dependencies(BaseModel):
    name: Optional[str] = None
    gender: Optional[Gender] = None
    relationship: Optional[Relationship] = None
    date_of_birth: Optional[date] = None
    

    
