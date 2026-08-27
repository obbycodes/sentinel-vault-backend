from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class TelemetryLogResponse(BaseModel):
    id: int
    user_id: int | None
    event_type: str
    description: str
    timestamp: datetime

    class Config:
        from_attributes = True