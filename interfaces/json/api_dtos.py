from pydantic import BaseModel, Field
from datetime import date
from enum import Enum
from typing import Optional, List

'''
Enums
'''
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
    tuition_fee_incr_perc: Optional[int] = None
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
    expense_type: str
    description: str
    expense_started_date: date
    expense_end_date: date
    
class Income(BaseModel):
    user_detail_id: int
    income_amount: float
    income_type: str
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
    description: str
    rank: str
    industry: str

class UserDetail(BaseModel):
    year_business: Optional[int] = None
    retirement_age: Optional[int] = None
    retirement_package: Optional[float] = None
    life_expectancy: Optional[int] = None
    
class UserRegister(BaseModel):
    first_name: str
    middle_name: Optional[str] = None
    last_name: str
    email_address: str
    date_of_birth: date
    marital: Optional[Marital] = None
    occupation: Optional[Occupation] = None
    user_detail: Optional[UserDetail] = None
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
    is_locked: Optional[int] = None
    
class Dependencies(BaseModel):
    name: Optional[str] = None
    gender: Optional[Gender] = None
    relationship: Optional[Relationship] = None
    date_of_birth: Optional[date] = None
    
class DependenciesPostJson(BaseModel):
    name: str
    gender: Gender
    relationship: Relationship
    date_of_birth: date
    
# Auth

class GrantType(str, Enum):
    password = "password"
    refresh = "refresh"
    
class AuthenticationJson(BaseModel):
    username: str
    password: str
    grant_type: GrantType