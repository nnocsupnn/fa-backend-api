from pydantic import BaseModel, Field
from datetime import date, datetime
from enum import Enum
from typing import Optional, List


# Income
class IncomeResponseJson(BaseModel):
    id: Optional[int] = None
    description: Optional[str] = None
    income_end_date: Optional[date] = None
    created_date: Optional[datetime] = None
    income_amount: Optional[float] = None
    user_detail_id: Optional[int] = None
    income_started_date: Optional[date] = None
    active: Optional[int] = None
    updated_date: Optional[datetime] = None


class IncomeProtectionProvisionResponseJson(BaseModel):
    id: Optional[int] = None
    income_protection_id: Optional[int] = None
    amount: Optional[float] = None
    created_date: Optional[datetime] = None
    updated_date: Optional[datetime] = None
    
class IncomeProtectionResponseJson(BaseModel):
    user_id: Optional[int] = None
    created_date: Optional[datetime] = None
    id: Optional[int] = None
    date_started: Optional[date] = None
    updated_date: Optional[datetime] = None
    income_protection_provision: List[IncomeProtectionProvisionResponseJson] = None
    

     
# Expenses
class ExpenseResponseJson(BaseModel):
    expense_category: Optional[str] = None
    id: Optional[int] = None
    expense_started_date: Optional[date] = None
    active: Optional[int] = None
    updated_date: Optional[datetime] = None
    user_detail_id: Optional[int] = None
    expense_amount: Optional[float] = None
    description: Optional[str] = None
    expense_end_date: Optional[date] = None
    created_date: Optional[datetime] = None
    
# Dependencies
class DependenciesResponseJson(BaseModel):
    id: Optional[int] = None
    gender: Optional[str] = None
    date_of_birth: Optional[date] = None
    created_date: Optional[datetime] = None
    name: Optional[str] = None
    user_id: Optional[int] = None
    relationship: Optional[str] = None
    dependency_detail_id: Optional[int] = None
    updated_date: Optional[datetime] = None
    
class DependencyProvisionResponseJson(BaseModel):
    id: Optional[str] = None
    created_date: Optional[datetime] = None
    amount: Optional[float] = None
    updated_date: Optional[datetime] = None
    
class DependencyDetailResponseJson(BaseModel):
    id: Optional[int] = None
    target_entry_age: Optional[int] = None
    dependency_provision_id: Optional[int] = None
    primary_lvl_annual: Optional[float] = None
    tertiary_lvl_annual: Optional[float] = None
    secondary_lvl_years: Optional[int] = None
    tuition_fee_incr_perc: Optional[float] = None
    updated_date: Optional[datetime] = None
    age_before_entry: Optional[int] = None
    secondary_lvl_annual: Optional[float] = None
    primary_lvl_years: Optional[int] = None
    tertiary_lvl_years: Optional[int] = None
    created_date: Optional[datetime] = None
    dependency_provision: Optional[DependencyProvisionResponseJson] = None
    
class DependenciesResponseJsonFull(BaseModel):
    id: Optional[int] = None
    gender: Optional[str] = None
    date_of_birth: Optional[date] = None
    created_date: Optional[datetime] = None
    name: Optional[str] = None
    user_id: Optional[int] = None
    relationship: Optional[str] = None
    dependency_detail_id: Optional[int] = None
    updated_date: Optional[datetime] = None
    dependency_detail: Optional[DependencyDetailResponseJson] = None
# User Detail

class ExpenseResponseJson(BaseModel):
    expense_category: Optional[str] = None
    id: Optional[int] = None
    expense_started_date: Optional[date] = None
    active: Optional[int] = None
    updated_date: Optional[datetime] = None
    user_detail_id: Optional[int] = None
    expense_amount: Optional[float] = None
    description: Optional[str] = None
    expense_end_date: Optional[date] = None
    created_date: Optional[datetime] = None

class IncomeResponseJson(BaseModel):
    description: Optional[str] = None
    id: Optional[int] = None
    income_end_date: Optional[date] = None
    created_date: Optional[datetime] = None
    user_detail_id: Optional[int] = None
    income_amount: Optional[float] = None
    income_started_date: Optional[date] = None
    active: Optional[int] = None
    updated_date: Optional[datetime] = None

class UserDetailResponseJson(BaseModel):
    user_id: Optional[int] = None
    year_business: Optional[int] = None
    retirement_package: Optional[float] = None
    id: Optional[int] = None
    retirement_age: Optional[int] = None
    life_expectancy: Optional[int] = None
    expenses: Optional[List[ExpenseResponseJson]] = []
    incomes: Optional[List[IncomeResponseJson]] = []
    
    
# Templates

class Categories(str, Enum):
    expenses = "expenses"
    education = "education"
    rank = "rank"
    industry = "industry"
    expenses_category = "expenses_category"
    
class TextTemplatesResponseJson(BaseModel):
    code: Optional[str] = None
    description: Optional[str] = None
    category: Optional[Categories] = None
    updated_date: Optional[datetime] = None
    created_date: Optional[datetime] = None
    id: Optional[int] = None

    
# Auth
class GrantType(str, Enum):
    password = "password"
    refresh = "refresh"
    
class AuthenticationJson(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    grant_type: GrantType
    
class JwtResponseJson(BaseModel):
    accessToken: str
    refreshToken: str
    expires: int
    
class SuccessResponseJson(BaseModel):
    code: Optional[int] = 200
    message: Optional[str] = "Done"