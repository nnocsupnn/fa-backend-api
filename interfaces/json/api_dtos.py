from pydantic import BaseModel, Field
from datetime import date
from enum import Enum
from typing import Optional

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
    
class Marital(str, Enum):
    single = "single"
    married = "married"
    divorced = "divorced"
    separated = "separated"
    widowed = "widowed"

'''
Models
'''
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
    first_name: str
    middle_name: Optional[str] = None
    last_name: str
    email_address: str
    date_of_birth: date
    marital: Optional[Marital] = None
    occupation: Optional[Occupation] = None
    user_detail: Optional[UserDetail] = None
    
class Dependencies(BaseModel):
    user_id: int
    name: str
    gender: Gender
    relationship: Relationship
    date_of_birth: date
    
class DependencyDetail(BaseModel):
    dependency_id: int
    type: str
    target_years: int
    target_entry_age: int
    age_before_entry: int
    amount: float
    
class DependencyProvision(BaseModel):
    user_id: int
    amount: float
    
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
    code: str
    description: str
    category: str


# Auth

class GrantType(str, Enum):
    password = "password"
    refresh = "refresh"
    
class AuthenticationJson(BaseModel):
    username: str
    password: str
    grant_type: GrantType