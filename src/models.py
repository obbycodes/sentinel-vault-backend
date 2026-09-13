from datetime import datetime, timezone
from typing import Any

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "users"
    id = Column[int](Integer, primary_key=True, index=True)
    username = Column[str](String, unique=True, index=True, nullable=False)
    email = Column[str](String, unique=True, index=True, nullable=False)
    hashed_password = Column[str](String, nullable=False)
    role = Column[str](String, default="Viewer", nullable=False)


class UserTelemetryLog(Base):
    __tablename__ = "telemetry_logs"
    id = Column[int](Integer, primary_key=True, index=True)
    user_id = Column[str](String, ForeignKey("users.id"), index=True)
    event_type = Column[str](String, index=True)
    description = Column[str](String, nullable=False)
    timestamp = Column[datetime](DateTime, default=lambda: datetime.now(timezone.utc))

    user = relationship("User")


class DeviceTelemetryLog(Base):
    __tablename__ = "device_telemetry"

    id = Column[int](Integer, primary_key=True, index=True)
    device_id = Column[str](String, index=True, nullable=False)
    cpu_usage = Column[Any](Float, nullable=False)
    memory_usage = Column[Any](Float, nullable=False)
    status = Column[str](String, default="NORMAL")
    timestamp = Column[datetime](DateTime, default=lambda: datetime.now(timezone.utc))
