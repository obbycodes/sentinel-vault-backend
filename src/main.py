from datetime import datetime, timezone
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query, Request, Response
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from sqlalchemy import func
from sqlalchemy.orm import Session

import models
from auth import UserRole, allow_roles
from database import engine, get_db
from schemas import TelemetrySubmit, UserChange, UserCreate, UserLogin
from security import (
    attach_auth_cookie,
    create_access_token,
    evaluate_device_anomalies,
    hash_password,
    log_audit_event,
    verify_password,
)

app = FastAPI(
    title="SentinelVault",
    description="Asset Management and Telemetry System",
    version="0.1.0",
)

DbSession = Annotated[Session, Depends(get_db)]
AdminUser = Annotated[models.User, Depends(allow_roles([UserRole.ADMIN]))]
PrivilegedUser = Annotated[
    models.User, Depends(allow_roles({UserRole.ADMIN, UserRole.ANALYST}))
]
AuthenticatedUser = Annotated[
    models.User,
    Depends(allow_roles({UserRole.ADMIN, UserRole.ANALYST, UserRole.VIEWER})),
]

models.Base.metadata.create_all(bind=engine)

limiter = Limiter(key_func=get_remote_address)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)

    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

    return response


@app.get("/")
def root_info():
    return {
        "app_name": "SentinelVault",
        "app_description": "Asset Management and Telemetry System",
        "app_version": "0.1.0",
    }


@app.get("/health")
def health_check(db: DbSession):
    return {
        "status": "System is at a healthy state.",
        "database_status": "Connected",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.post("/api/register", status_code=201)
@limiter.limit("5/minute")
def register_user(request: Request, user_data: UserCreate, db: DbSession):
    existing_user = (
        db.query(models.User).filter(models.User.username == user_data.username).first()
    )
    if existing_user:
        raise HTTPException(409, "User already exists.")

    hashed_pwd = hash_password(user_data.password)

    new_user = models.User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_pwd,
        role="Viewer",
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User successfully registered!", "user_id": new_user.id}


@app.post("/api/login")
@limiter.limit("5/minute")
def login_user(
    request: Request,
    response: Response,
    credentials: UserLogin,
    db: DbSession,
):
    user = (
        db.query(models.User)
        .filter(models.User.username == credentials.username)
        .first()
    )

    if not user or not verify_password(credentials.password, user.hashed_password):
        log_audit_event(
            db,
            "LOGIN_FAILED",
            f"Failed login attempt from username: {credentials}",
            user_id=None,
        )
        raise HTTPException(status_code=401, detail="Invalid username or password.")

    token = create_access_token(
        {"username": user.username, "user_id": user.id, "role": user.role}
    )

    attach_auth_cookie(response, token)

    response_content = {
        "message": "Login successful!",
        "username": user.username,
        "role": user.role,
    }

    log_audit_event(
        db,
        "LOGIN_SUCCESS",
        f"Successful login attempt from {credentials.username}",
        user_id=user.id,
    )
    return response_content


@app.get("/api/admin/system-reset")
def reset_system(current_user: AdminUser):
    return {"message": "System reset executed."}


@app.post("/api/admin/change-role")
def change_role(
    payload: UserChange,
    current_user: PrivilegedUser,
    db: DbSession,
):
    user = (
        db.query(models.User).filter(models.User.username == payload.username).first()
    )

    if not user:
        raise HTTPException(404, "User not found.")

    user.role = payload.new_role

    db.commit()
    db.refresh(user)

    return {"message": f"{user.username}'s role changed.", "new_role": f"{user.role}"}


@app.get("/api/telemetry/logs")
def get_audit_logs(
    db: DbSession,
    current_user: PrivilegedUser,
):

    logs = (
        db.query(models.UserTelemetryLog)
        .filter(models.UserTelemetryLog.timestamp)
        .all()
    )
    return logs


@app.post("/api/telemetry/submit")
def submit_telemetry_logs(
    data: TelemetrySubmit,
    db: DbSession,
    current_user: PrivilegedUser,
):

    submission_entry = models.DeviceTelemetryLog(
        device_id=data.device_id,
        cpu_usage=data.cpu_usage,
        memory_usage=data.memory_usage,
        status=data.status,
    )

    is_anomaly = evaluate_device_anomalies(db, submission_entry, current_user.id)

    db.add(submission_entry)
    db.commit()
    db.refresh(submission_entry)

    return {
        "message": "Telemetry logged successfully",
        "device_id": f"{data.device_id}",
        "anomaly_flagged": f"{is_anomaly}",
        "status": f"{data.status}",
        "timestamp": f"{datetime.now(timezone.utc)}",
    }


@app.get("/api/telemetry/query")
def telemetry_query(
    db: DbSession,
    current_user: AuthenticatedUser,
    device_id: str | None = None,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    offset: Annotated[int, Query(ge=0)] = 0,
):

    query = db.query(models.DeviceTelemetryLog)

    if device_id:
        query = query.filter(models.DeviceTelemetryLog.device_id == device_id)

    records = (
        query.order_by(models.DeviceTelemetryLog.timestamp.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    return records


@app.get("/api/telemetry/stats")
def get_telemetry_stats(db: DbSession, current_user: AuthenticatedUser):
    metrics = (
        db.query(func.count(models.DeviceTelemetryLog.id)).label("total_records"),
        db.query(func.count(func.distinct(models.DeviceTelemetryLog.device_id))).label(
            "total_devices"
        ),
        db.query(func.avg(models.DeviceTelemetryLog.cpu_usage)).label("avg_cpu_usage"),
        db.query(func.avg(models.DeviceTelemetryLog.memory_usage)).label(
            "avg_ram_usage"
        ),
        db.query(
            func.count(models.DeviceTelemetryLog.id).filter(
                models.DeviceTelemetryLog.status == "CRITICAL"
            )
        ).label("anomalies"),
    ).first()
    return {
        "total_records": metrics.total_records or 0,
        "total_devices": metrics.total_devices or 0,
        "avg_cpu_usage": metrics.avg_cpu_usage or 0,
        "avg_ram_usage": metrics.avg_ram_usage or 0,
        "anomalies": metrics.anomalies or 0,
    }
