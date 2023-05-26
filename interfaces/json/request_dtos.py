from pydantic import BaseModel, Field
from datetime import date, datetime
from enum import Enum
from interfaces.json import Gender, Relationship
from typing import Optional, List

class IncomePostJson(BaseModel):
    description: str
    income_end_date: Optional[date] = None
    income_amount: float
    income_started_date: Optional[date] = None
    active: Optional[int] = None
    
class ExpensePostJson(BaseModel):
    expense_category: str
    description: str
    active: Optional[int] = None
    expense_amount: float
    expense_started_date: Optional[date] = None
    expense_end_date: Optional[date] = None
    
class IncomePatchJson(BaseModel):
    income_amount: Optional[float] = None
    description: Optional[str] = None
    income_started_date: Optional[date] = None
    income_end_date: Optional[date] = None
    
class ExpensePatchJson(BaseModel):
    expense_amount: Optional[float] = None
    description: Optional[str] = None
    expense_started_date: Optional[date] = None
    expense_end_date: Optional[date] = None
    expense_category: Optional[str] = None
    active: Optional[int] = None

class DependenciesPostJson(BaseModel):
    name: str
    gender: Gender
    relationship: Relationship
    date_of_birth: date
    
class IncomeProtectionProvisionPostJson(BaseModel):
    amount: Optional[float] = 0
    
class IncomeProtectionPostJson(BaseModel):
    date_started: Optional[date] = None
    income_protection_provision: list[IncomeProtectionProvisionPostJson] = None
   
class IncomeProtectionProvisionPatchJson(BaseModel):
    amount: float
    
class IncomeProtectionPatchJson(BaseModel):
    date_started: date
    
class LifestyleProtectionPatchJson(BaseModel):
    existing_provision: Optional[float] = Field(description="Existing Provision", default=None)
    source_fund: Optional[float] = Field(description="Source Fund", default=None)
    gov_fund: Optional[float] = Field(description="Government Fund", default=None)
    other_fund: Optional[float] = Field(description="Other Fund", default=None)
    
class LifestyleProtectionInvestmentsPostJson(BaseModel):
    age: int
    annual_investment: float
    projection_rate: float
    
class LifestyleProtectionInvestmentsPatchJson(BaseModel):
    age: Optional[int] = None
    annual_investment: float
    projection_rate: float
    
class WealthPatchJson(BaseModel):
    real_properties_value: Optional[float] = None
    personal_properties_value: Optional[float] = None
    liquid_investments_value: Optional[float] = None
    projected_apprec_rate_per_year: Optional[float] = None
    projected_rate_return_on_fixed: Optional[float] = None
    other_investment_value: Optional[float] = None
    tax_rate: Optional[float] = None
    
class KapritsoPatchJson(BaseModel):
    factor: Optional[float] = None
    daily_cost: Optional[float] = None
    
class ConfigPatchJson(BaseModel):
    inflation_rate: float
    deduction_from_family_home: float
    other_deduction: float