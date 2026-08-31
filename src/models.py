from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Float
from database import Base
from datetime import datetime, timezone
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    id = Column[int](Integer, primary_key=True, index=True)
    username = Column[str](String, unique=True, index=True, nullable=False)
    email = Column[str](String, unique=True, index=True, nullable=False)
    hashed_password = Column[str](String, nullable=False)

    role = Column[str](String, default="Viewer", nullable=False)

class TelemetryLog(Base):
    __tablename__ = "telemetry_logs"

    id = Column[int](Integer, primary_key=True, index=True)
    user_id = Column[str](String, ForeignKey("users.id"), index=True)
    event_type = Column[str](String, index=True)
    description = Column[str](String)
    timestamp = Column[datetime](DateTime, default=lambda: datetime.now(timezone.utc))

    user = relationship("User")

class DeviceTelemetry(Base):
    __tablename__ = "device_telemetry"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String, index=True, nullable=False)
    cpu_usage = Column(Float, nullable=False)
    memory_usage = Column(Float, nullable=False)
    status = Column(String, default="NORMAL")
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
