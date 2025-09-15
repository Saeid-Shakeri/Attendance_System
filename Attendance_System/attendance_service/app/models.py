from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from database import Base

class AttendanceRecord(Base):
    __tablename__ = "attendance_records"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, index=True)
    action = Column(String)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)