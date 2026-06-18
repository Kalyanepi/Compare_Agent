from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class CompareRequest(BaseModel):
    policy_a: str
    policy_b: str

class ClauseCompare(BaseModel):
    clause: str
    policy_a_value: str
    policy_b_value: str
    difference: str

class ComparisonResult(BaseModel):
    summary: str
    clauses: List[ClauseCompare]

class ComparisonOut(BaseModel):
    id: str
    status: str
    result: Optional[ComparisonResult] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
