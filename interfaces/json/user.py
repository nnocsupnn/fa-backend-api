from pydantic import BaseModel
from datetime import date
from enum import Enum
from typing import Optional

class Marital(str, Enum):
    single = "single"
    married = "married"
    divorced = "divorced"
    separated = "separated"
    widowed = "widowed"

class Occupation(BaseModel):
    description: str
    rank: str
    industry: str

class User(BaseModel):
    first_name: str
    middle_name: str
    last_name: str
    email_address: str
    date_of_birth: date
    marital: Marital
    occupation: Optional[Occupation] = None