from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional

class AttendanceRecordCreate(BaseModel):
    employee_id: int
    action: str  # "in" or "out"

class AttendanceRecordResponse(BaseModel):
    id: int
    employee_id: int
    action: str
    timestamp: datetime
    
    class Config:
        from_attributes = True

class TokenData(BaseModel):
    username: str
    role: str