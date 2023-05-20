from pydantic import BaseModel, Field
from datetime import date
from enum import Enum
from typing import Optional, List


# Income
class IncomeResponseJson(BaseModel):
    id: Optional[int] = None
    description: Optional[str] = None
    income_end_date: Optional[date] = None
    created_date: Optional[date] = None
    income_amount: Optional[float] = None
    user_detail_id: Optional[int] = None
    income_started_date: Optional[date] = None
    active: Optional[int] = None
    updated_date: Optional[date] = None

# Expenses
class ExpenseResponseJson(BaseModel):
    expense_category: Optional[str] = None
    id: Optional[int] = None
    expense_started_date: Optional[date] = None
    active: Optional[int] = None
    updated_date: Optional[date] = None
    user_detail_id: Optional[int] = None
    expense_amount: Optional[float] = None
    description: Optional[str] = None
    expense_end_date: Optional[date] = None
    created_date: Optional[date] = None
    
# Dependencies
class DependenciesResponseJson(BaseModel):
    id: Optional[int] = None
    gender: Optional[str] = None
    date_of_birth: Optional[date] = None
    created_date: Optional[date] = None
    name: Optional[str] = None
    user_id: Optional[int] = None
    relationship: Optional[str] = None
    dependency_detail_id: Optional[int] = None
    updated_date: Optional[date] = None
    
class DependencyProvisionResponseJson(BaseModel):
    id: Optional[str] = None
    created_date: Optional[date] = None
    amount: Optional[float] = None
    updated_date: Optional[date] = None
    
class DependencyDetailResponseJson(BaseModel):
    id: Optional[int] = None
    target_entry_age: Optional[int] = None
    dependency_provision_id: Optional[int] = None
    primary_lvl_annual: Optional[float] = None
    tertiary_lvl_annual: Optional[float] = None
    secondary_lvl_years: Optional[int] = None
    tuition_fee_incr_perc: Optional[float] = None
    updated_date: Optional[date] = None
    age_before_entry: Optional[int] = None
    secondary_lvl_annual: Optional[float] = None
    primary_lvl_years: Optional[int] = None
    tertiary_lvl_years: Optional[int] = None
    created_date: Optional[date] = None
    dependency_provision: Optional[DependencyProvisionResponseJson] = None
    
# Auth

class GrantType(str, Enum):
    password = "password"
    refresh = "refresh"
    
class AuthenticationJson(BaseModel):
    username: str
    password: str
    grant_type: GrantType
    
class JwtResponseJson(BaseModel):
    accessToken: str
    refreshToken: str
    expires: int