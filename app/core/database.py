# Import necessary modules from SQLAlchemy and project-specific modules.
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.settings import postgres_settings, redis_settings
import redis

# Create the database engine using the URL
engine = create_engine(postgres_settings.__str__())

# Create a session maker to interact with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get a database session
def get_db():
    # Create a new session
    db = SessionLocal()
    try:
        # Yield the session to be used by the caller
        yield db
    finally:
        # Close the session when done
        db.close()

# Redis connection
redis_client = redis.StrictRedis(host=redis_settings.REDIS_HOSTNAME, port=redis_settings.REDIS_PORT, db=1)