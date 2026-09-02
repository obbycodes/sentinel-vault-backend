from fastapi import FastAPI, Depends, HTTPException, Response, Request, status, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from typing import Optional, Annotated
from pydantic import Field
import models
import schemas
from database import engine, get_db
from schemas import UserCreate, UserLogin
from security import hash_password, verify_password, create_access_token, decode_access_token

models.Base.metadata.create_all(bind=engine) ## Create all tables in the database

limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="SentinelVault",
    description="Enterprise Asset & Secure Telemetry Platform",
    version="0.4.0",
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "no-referrer-when-downgrade"

    return response

@app.get("/")
def read_root():
    return {
        "system": "SentinelVault Telemetry Engine",
        "status": "operational",
        "version": "0.4.0"
    }

@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    return {
        "status": "healthy",
        "database": "connected"
    }


@app.post("/api/register", 
responses={
    409:{"description":"Conflict", "content": {"application.json": {"example": {"detail": {"User already registered."}}}}}, 
    429:{"description":"Too Many Requests", "content": {"application.json": {"example": {"detail": {"Rate limit exceeded. 3 per 1 minute."}}}}}
},
    status_code=status.HTTP_201_CREATED)
@limiter.limit("3/minute")
def register_user(request: Request, user_data: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(status_code=409, detail="User already registered.")
    
    hashed_pwd = hash_password(user_data.password)

    new_user = models.User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_pwd,
        role="Viewer"
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User successfully registered!", "user_id": new_user.id}


@app.post("/api/login", 
responses={
    401:{"description":"Unauthorized", "content": {"application.json": {"example": {"detail": {"Invalid username or password."}}}}},
    429:{"description":"Too Many Requests", "content": {"application.json": {"example": {"detail": {"Rate limit exceeded: 3 per 1 minute."}}}}}
})
@limiter.limit("3/minute")
def login_user(request: Request, credentials: UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == credentials.username).first()

    if not user or not verify_password(credentials.password, user.hashed_password):
        log_audit_event(db, "LOGIN_FAILED", f"Failed login attempt for username: {credentials}.", user_id=None)
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    token = create_access_token({
        "username": user.username,
        "user_id": user.id,
        "role": user.role
    })

    response_content = {
        "message": "Login successful!",
        "username": user.username,
        "role": user.role
    }
    response = JSONResponse(content=response_content)

    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=False,
        samesite="lax"
    )

    log_audit_event(db, "LOGIN_SUCCESS", "User logged in successfully", user_id=user.id)

    return response


def get_current_user(request: Request, db: Session = Depends(get_db)):

    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated: No session cookie")
    
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    user = db.query(models.User).filter(models.User.id == payload.get("user_id")).first()
    if not user:
        raise HTTPException(status_code=404, detail="User account no longer exists")

    return user

class RoleChecker:
    def __init__(self, allowed_roles: list[str]):
        self.allowed_roles = allowed_roles
    
    def __call__(self, current_user: models.User = Depends(get_current_user)):
        if current_user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied: Role '{current_user.role}' lacks permission to access this resource."
            )
        return current_user

@app.get("/api/dashboard", 
    responses={
    429:{"description":"Too Many Requests", "content": {"application.json": {"example": {"detail": {"Rate limit exceeded. 10 per minute."}}}}}
    },
)
@limiter.limit("10/minute")
def view_dashboard(request: Request, current_user: models.User = Depends(RoleChecker(["Admin", "Analyst", "Viewer"]))):
    return {"message": "Welcome to the public telemetry dashboard."}

@app.get("/api/telemetry/metrics",
    responses={
        429:{"description":"Too Many Requests", "content": {"application.json": {"example": {"detail": {"Rate limit exceeded. 7 per minute."}}}}}
    },
)
@limiter.limit("7/minute")
def view_metrics(request: Request, current_user: models.User = Depends(RoleChecker(["Admin", "Analyst", ]))):
    return {"message": "Sensitive system metrics", "data": {"cpu_load": "12%", "ram_usage": "45%"}}

@app.get("/api/telemetry/system_reset", 
    responses={
        429:{"description":"Too Many Requests", "content": {"application.json": {"example": {"detail": {"Rate limit exceeded. 1 per minute."}}}}}
    },
)
@limiter.limit("1/minute")
def system_reset(request: Request, current_user: models.User = Depends(RoleChecker(["Admin"]))):
    return {"message": "System settings accessed successfully."}

@app.get("/api/me", 
    responses={
        429:{"description":"Too Many Requests", "content": {"application.json": {"example": {"detail": {"Rate limit exceeded. 10 per minute."}}}}}
    },
)
@limiter.limit("10/minute")
def get_my_profile(request: Request, current_user: models.User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "role": current_user.role
    }


def log_audit_event(db: Session, event_type: str, description: str, user_id: int | None):
    log_entry = models.TelemetryLog(
        user_id=user_id,
        event_type=event_type,
        description=description
    )
    db.add(log_entry)
    db.commit()


@app.get("/api/telemetry/logs", 
    responses={
        429:{"description":"Too Many Requests", "content": {"application.json": {"example": {"detail": {"Rate limit exceeded. 5 per minute."}}}}}
    },
    response_model=list[schemas.TelemetryLogResponse]
)
@limiter.limit("5/minute") 

def get_audit_logs(
    request: Request,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(RoleChecker(["Admin", "Analyst"]))
):
    logs = db.query(models.TelemetryLog).order_by(models.TelemetryLog.timestamp.description)
    return logs

@app.post("/api/telemetry/submit", status_code=status.HTTP_201_CREATED)
def submit_telemetry(
    data: schemas.TelemetrySubmit,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(RoleChecker(["Admin", "Analyst"]))
):
    # 1. Instantiate telemetry model using sanitized inputs
    entry = models.DeviceTelemetry(
        device_id=data.device_id,
        cpu_usage=data.cpu_usage,
        memory_usage=data.memory_usage,
        status=data.status
    )
    
    # 2. Persist using parameterized SQLAlchemy query
    db.add(entry)
    db.commit()
    db.refresh(entry)
    
    is_anomaly = evaluate_device_anomalies(db, entry, user_id=current_user.id)

    # 3. Write event to audit log
    log_audit_event(
        db, 
        event_type="TELEMETRY_INGESTED", 
        description=f"Device {data.device_id} reported CPU: {data.cpu_usage}%", 
        user_id=current_user.id
    )
    
    return {"message": "Telemetry recorded successfully", 
            "telemetry_id": entry.id,
            "anomaly_flagged": is_anomaly,
            "status": entry.status}

@app.get("/api/telemetry/query", response_model=list[schemas.DeviceTelemetryResponse])
def query_telemetry(
    device_id: Optional[str] = None,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    offset: Annotated[int, Query(ge=0)] = 0,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(RoleChecker(["Admin", "Analyst", "Viewer"]))
):
    # 1. Start base query
    query = db.query(models.DeviceTelemetry)
    
    # 2. Apply optional device_id filter
    if device_id:
        query = query.filter(models.DeviceTelemetry.device_id == device_id)
        
    # 3. Apply sorting (newest first) and pagination window
    records = query.order_by(models.DeviceTelemetry.timestamp.desc()).offset(offset).limit(limit).all()
    
    return records

def evaluate_device_anomalies(db: Session, telemetry_entry: models.DeviceTelemetry, user_id: int):
    CPU_THRESHOLD = 85.0
    MEMORY_THRESHOLD = 90.0
    
    anomalies = []
    if telemetry_entry.cpu_usage > CPU_THRESHOLD:
        anomalies.append(f"High CPU utilization ({telemetry_entry.cpu_usage}%)")
    if telemetry_entry.memory_usage > MEMORY_THRESHOLD:
        anomalies.append(f"High Memory utilization ({telemetry_entry.memory_usage}%)")
        
    if anomalies:
        # 1. Update telemetry status in database
        telemetry_entry.status = "CRITICAL"
        db.commit()
        
        # 2. Record critical security alert in telemetry logs
        details = f"Anomaly detected on {telemetry_entry.device_id}: " + ", ".join(anomalies)
        log_audit_event(
            db, 
            event_type="CRITICAL_ANOMALY", 
            description=details, 
            user_id=user_id
        )
        return True
    return False

