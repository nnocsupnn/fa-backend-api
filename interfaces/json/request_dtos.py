from pydantic import BaseModel, Field
from datetime import date, datetime
from enum import Enum
from typing import Optional, List

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
    existing_provision: Optional[float] = None
    source_fund: Optional[float] = None
    gov_fund: Optional[float] = None
    other_fund: Optional[float] = None
    
class LifestyleProtectionInvestmentsPostJson(BaseModel):
    age: int
    annual_investment: float
    projection_rate: float
    
class LifestyleProtectionInvestmentsPatchJson(BaseModel):
    age: int
    annual_investment: float
    projection_rate: float
    
class WealthPatchJson(BaseModel):
    real_properties_value: Optional[float] = None
    personal_properties_value: Optional[float] = None
    liquid_investments_value: Optional[float] = None
    projected_apprec_rate_per_year: Optional[float] = None
    projected_rate_return_on_fixed: Optional[float] = None
    tax_rate: Optional[float] = None
    
class KapritsoPatchJson(BaseModel):
    factor: Optional[float] = None
    daily_cost: Optional[float] = None