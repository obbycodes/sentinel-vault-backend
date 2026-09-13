from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class TelemetrySubmit(BaseModel):
    device_id: str = Field(min_length=3, max_length=50)
    cpu_usage: float = Field(ge=0.0, le=100.0)
    memory_usage: float = Field(ge=0.0, le=100.0)
    status: str = Field(pattern="^(NORMAL|WARNING|CRITICAL)$")


class DeviceTelemetryResponse(BaseModel):
    id: int
    device_id: str
    cpu_usage: float
    memory_usage: float
    status: str
    timestamp: datetime


class UserChange(BaseModel):
    username: str
    new_role: str
