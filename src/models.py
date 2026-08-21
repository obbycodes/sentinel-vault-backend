from sqlalchemy import Column, Integer, String, DateTime, Boolean
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column[int](Integer, primary_key=True, index=True)
    username = Column[str](String, unique=True, index=True, nullable=False)
    email = Column[str](String, unique=True, index=True, nullable=False)
    hashed_password = Column[str](String, nullable=False)

    role = Column[str](String, default="Viewer", nullable=False)