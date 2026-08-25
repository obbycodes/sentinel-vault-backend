from fastapi import FastAPI, Depends, HTTPException, Response, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import models
from database import engine, get_db
from schemas import UserCreate, UserLogin
from security import hash_password, verify_password, create_access_token, decode_access_token

models.Base.metadata.create_all(bind=engine) ## Create all tables in the database

app = FastAPI(
    title="SentinelVault",
    description="Enterprise Asset & Secure Telemetry Platform",
    version="0.2.0",
)

@app.get("/")
def read_root():
    return {
        "system": "SentinelVault Telemetry Engine",
        "status": "operational",
        "version": "0.2.0",
    }

@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    return {
        "status": "healthy",
        "database": "connected"
    }

@app.post("/api/register", status_code=status.HTTP_201_CREATED)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered.")
    
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

@app.post("/api/login")
def login_user(credentials: UserLogin, response: Response, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == credentials.username).first()

    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    token = create_access_token({
        "sub": user.username,
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

@app.get("/api/me")
def get_my_profile(current_user: models.User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "role": current_user.role
    }
