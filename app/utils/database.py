from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from pydantic import BaseSettings, PostgresDsn, Field
from contextlib import contextmanager
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    DATABASE_URL: PostgresDsn = Field(..., env="DATABASE_URL")

    class Config:
        env_file = ".env"

settings = Settings()

# Try to create an engine or handle the exception if connection fails
try:
    engine = create_engine(settings.DATABASE_URL)
except Exception as e:
    logger.error(f"Error connecting to the database: {e}")
    raise e  # Optionally raise an exception or handle it differently depending on your application's needs

# Using scoped session to ensure thread safety in a web application context
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()

@contextmanager
def get_db():
    """
    Provides a transactional scope around a series of operations.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Example usage
if __name__ == "__main__":
    with get_db() as session:
        # perform database operations
        pass
