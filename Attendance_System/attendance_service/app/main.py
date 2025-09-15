from fastapi import FastAPI, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from datetime import datetime
from pydantic import BaseModel
from typing import Union
from jose import JWTError, jwt
from dotenv import load_dotenv
import models, schemas, database
import requests, os


load_dotenv()

AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL")

app = FastAPI(title="Attendance Service", docs_url="/docs")

async def get_current_user(authorization: str = Header(..., alias="Authorization")):
    if not authorization :
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    token = authorization.split(" ")[1]
    try:
        response = requests.get(
            f"{AUTH_SERVICE_URL}/users/me",
            headers={"Authorization": f"Bearer {token}"},
            timeout=5
        )
        
        if response.status_code == 200:
            user_data = response.json()
            return user_data
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )
            
    except requests.RequestException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Auth service unavailable",
        )

@app.on_event("startup")
async def startup():
    models.Base.metadata.create_all(bind=database.engine)


@app.post("/attendance", response_model=schemas.AttendanceRecordResponse)
async def create_attendance_record(
    record: schemas.AttendanceRecordCreate,
    db: Session = Depends(database.get_db),
    current_user: dict = Depends(get_current_user)
    ):
    if record.action not in ["in", "out"]:
        raise HTTPException(status_code=400, detail="Action must be 'in' or 'out'")
    
    if not is_admin(current_user) and current_user.get('employee_id') != record.employee_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only record attendance for yourself"
        )
    
    db_record = models.AttendanceRecord(
        employee_id=record.employee_id,
        action=record.action,
        timestamp=datetime.now()
    )
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    
    return db_record


@app.get("/attendance/{employee_id}")
async def get_attendance_records(
    employee_id: int,
    db: Session = Depends(database.get_db),
    current_user: dict = Depends(get_current_user)
    ):
    check_access_permission(current_user, employee_id)
    
    records = db.query(models.AttendanceRecord).filter(
        models.AttendanceRecord.employee_id == employee_id
    ).order_by(models.AttendanceRecord.timestamp.desc()).all()
    
    return records

@app.get("/attendance")
async def get_all_attendance_records(
    db: Session = Depends(database.get_db),
    current_user: dict = Depends(get_current_user)
    ):
    if not is_admin(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required to view all records"
        )
    
    records = db.query(models.AttendanceRecord).order_by(
        models.AttendanceRecord.timestamp.desc()
    ).all()
    
    return records


def is_admin(user: dict) -> bool:
    return user.get('is_admin', False)

def can_access_employee(current_user: dict, target_employee_id: int) -> bool:
    if is_admin(current_user):
        return True
    return current_user.get('employee_id') == target_employee_id

def check_access_permission(current_user: dict, target_employee_id: int):
    if not can_access_employee(current_user, target_employee_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to access this resource"
        )
