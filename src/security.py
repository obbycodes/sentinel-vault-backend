from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import Cookie, Depends, HTTPException, Response
from joserfc import jwk, jwt
from joserfc.errors import ClaimError, JoseError
from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher
from sqlalchemy.orm import Session

import models
from database import get_db
from models import DeviceTelemetryLog, UserTelemetryLog

pwd_context = PasswordHash((Argon2Hasher(),))

SECRET_KEY = jwk.import_key("placeholderplaceholderplaceholderplaceholder", "oct")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

GetDB = Annotated[Session, Depends(get_db)]

claims_verifier = jwt.JWTClaimsRegistry(  ## aka payload registry. Note to self.
    exp={"essential": True}
)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)


def create_access_token(data: dict) -> str:
    header = {"alg": ALGORITHM}
    claims = data.copy()  ## Reminder! Claims means payload.
    expire_time = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    claims.update({"exp": int(expire_time.timestamp())})

    token = jwt.encode(header, claims, SECRET_KEY)
    return token


def decode_access_token(token: str) -> dict | None:
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        claims_verifier.validate(decoded_token.claims)

        return decoded_token.claims
    except (JoseError, ClaimError):
        return None


def get_current_user(db: GetDB, access_token: str = Cookie(None)):
    if not access_token:
        raise HTTPException(status_code=401, detail="Not authenticated.")

    payload = decode_access_token(access_token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token.")

    user_id = payload.get("user_id")
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        raise HTTPException(401, "User not found")

    return user


def attach_auth_cookie(response: Response, token: str):
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        samesite="lax",
        secure=False,  ## set to True for HTTPS!
    )


def log_audit_event(
    db: Session, event_type: str, description: str, user_id: int | None
):
    log_entry = UserTelemetryLog(
        user_id=user_id, event_type=event_type, description=description
    )

    db.add(log_entry)
    db.commit()
    db.refresh(log_entry)


def evaluate_device_anomalies(db: Session, entry: DeviceTelemetryLog, user_id: int):
    CPU_THRESHOLD = 85.0
    MEMORY_THRESHOLD = 90.0

    anomalies = []

    if entry.cpu_usage > CPU_THRESHOLD:
        anomalies.append("High CPU utilization")
    if entry.memory_usage > MEMORY_THRESHOLD:
        anomalies.append("High memory utilization")

    if anomalies:
        entry.status = "CRITICAL"
        db.commit()

        log_audit_event(
            db=db,
            event_type="CRITICAL_ANOMALY",
            description=f"Anomaly detected on {entry.device_id}: {anomalies}",
            user_id=user_id,
        )
        return True
    return False
