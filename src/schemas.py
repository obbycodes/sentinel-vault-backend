from pydantic import BaseModel, EmailStr, Field
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

class TelemetrySubmit(BaseModel):
    device_id: str = Field(..., min_length=3, max_length=50, pattern=r"^[a-zA-Z0-9\-_]+$")
    cpu_usage: float = Field(..., ge=0.0, le=100.0)
    memory_usage: float = Field(..., ge=0.0, le=100.0)
    status: str = Field("NORMAL", max_length=20)