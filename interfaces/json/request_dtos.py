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