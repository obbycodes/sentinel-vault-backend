import os
import time
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./sentinel-vault.db")

if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

IS_TESTING = os.getenv("APP_ENV") == "testing" or not DATABASE_URL or DATABASE_URL.startswith("sqlite")

if IS_TESTING:
    if not DATABASE_URL:
        PROJECT_ROOT = Path(__file__).resolve().parent.parent

        db_file_path = PROJECT_ROOT / "sentinel-vault.db"

        DATABASE_URL = f"sqlite:///{db_file_path.as_posix()}"

MAX_RETRIES = 1 if IS_TESTING else 5
RETRY_DELAY = 2

for attempt in range(MAX_RETRIES):
    try:
        engine = create_engine(DATABASE_URL, connect_args=connect_args)
        with engine.connect() as connection:
            print("Successfully connected to the database engine!")
            break
    except OperationalError as e:
        if attempt == MAX_RETRIES - 1:
            print(f"Database connection failed after {MAX_RETRIES} attempts.")
            raise e
        print(f"Database container is booting up... Retrying in {RETRY_DELAY}s (Attempt {attempt + 1}/{MAX_RETRIES})")
        time.sleep(RETRY_DELAY)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
