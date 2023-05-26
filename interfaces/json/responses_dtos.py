from pydantic import BaseModel, Field
from datetime import date, datetime
from enum import Enum
from typing import Optional, List
from interfaces.json import Gender, UserLevel

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
    id: Optional[int] = None
    user_id: Optional[int] = None
    created_date: Optional[datetime] = None
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
    id: Optional[int] = None
    user_detail_id: Optional[int] = None
    expense_category: Optional[str] = None
    expense_amount: Optional[float] = None
    description: Optional[str] = None
    active: Optional[int] = None
    expense_started_date: Optional[date] = None
    expense_end_date: Optional[date] = None
    updated_date: Optional[datetime] = None
    created_date: Optional[datetime] = None

class IncomeResponseJson(BaseModel):
    id: Optional[int] = None
    user_detail_id: Optional[int] = None
    description: Optional[str] = None
    income_amount: Optional[float] = None
    active: Optional[int] = None
    income_started_date: Optional[date] = None
    income_end_date: Optional[date] = None
    created_date: Optional[datetime] = None
    updated_date: Optional[datetime] = None

class UserDetailResponseJson(BaseModel):
    id: Optional[int] = None
    user_id: Optional[int] = None
    year_business: Optional[int] = None
    retirement_package: Optional[float] = None
    retirement_age: Optional[int] = None
    life_expectancy: Optional[int] = None
    avg_annual_salary_incr: Optional[float] = Field(description="Average Annual Salary Increase", default=None)
    max_age_of_dependent: Optional[int] = 0
    min_age_of_dependent: Optional[int] = 0
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
    id: Optional[int] = None
    code: Optional[str] = None
    description: Optional[str] = None
    category: Optional[Categories] = None
    updated_date: Optional[datetime] = None
    created_date: Optional[datetime] = None

# Lifestyle Protection
class LifestyleProtectionResponseJson(BaseModel):
    id: Optional[int] = None
    user_id: Optional[int] = None
    source_fund: Optional[float] = None
    other_fund: Optional[float] = None
    updated_date: Optional[datetime] = None
    existing_provision: Optional[float] = None
    gov_fund: Optional[float] = None
    created_date: Optional[datetime] = None
    
class LifestyleProtectionInvestmentsResponseJson(BaseModel):
    id: Optional[int] = None
    user_id: Optional[int] = None
    age: Optional[int] = None
    projection_rate: Optional[float] = None
    annual_investment: Optional[float] = None
    created_date: Optional[datetime] = None
    updated_date: Optional[datetime] = None
    
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
    status: Optional[int] = 200
    message: Optional[str] = "Success"
    
class WealthResponseJson(BaseModel):
    id: Optional[int] = None
    user_id: Optional[int] = None
    real_properties_value: Optional[float] = None
    personal_properties_value: Optional[float] = None
    liquid_investments_value: Optional[float] = None
    projected_apprec_rate_per_year: Optional[float] = None
    projected_rate_return_on_fixed: Optional[float] = None
    other_investment_value: Optional[float] = None
    tax_rate: Optional[float] = None
    created_date: Optional[datetime] = None
    updated_date: Optional[datetime] = None
    
class KapritsoResponseJson(BaseModel):
    id: Optional[int] = None
    user_id: Optional[int] = None
    factor: Optional[float] = None
    daily_cost: Optional[float] = None
    created_date: Optional[datetime] = None
    updated_date: Optional[datetime] = None
    
class OccupationResponseJson(BaseModel):
    id: Optional[int] = None
    description: Optional[str] = None
    rank: Optional[str] = None
    industry: Optional[str] = None
    
class UserResponseJson(BaseModel):
    id: Optional[int] = None
    marital: Optional[str] = None
    last_name: Optional[str] = None
    occupation_id: Optional[int] = None
    middle_name: Optional[str] = None
    user_level: Optional[UserLevel] = None
    gender: Optional[Gender] = None
    deletable: Optional[int] = None
    email_address: Optional[str] = None
    password: Optional[str] = None
    active: Optional[int] = None
    first_name: Optional[str] = None
    date_of_birth: Optional[date] = None
    basic_salary: Optional[float] = None
    net_salary: Optional[float] = None
    user_detail: Optional[UserDetailResponseJson] = None
    dependencies: list[DependenciesResponseJson] = []
    lifestyle_protection: Optional[LifestyleProtectionResponseJson] = None
    lifestyle_protection_investments: list[LifestyleProtectionInvestmentsResponseJson] = []
    kapritso: Optional[KapritsoResponseJson] = None
    wealth: Optional[WealthResponseJson] = None
    occupation: Optional[OccupationResponseJson] = None
    income_protection: Optional[IncomeProtectionResponseJson] = None
    
    
class ConfigResponseJson(BaseModel):
    id: Optional[int] = None
    inflation_rate: Optional[float] = None
    other_deduction: Optional[float] = None
    deduction_from_family_home: Optional[float] = None
    created_date: Optional[datetime] = None
    updated_date: Optional[datetime] = None
    