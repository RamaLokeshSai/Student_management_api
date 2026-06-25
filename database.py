import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. Define the Database URL.
# We check if a DATABASE_URL environment variable is provided (useful for deployment with persistent disks).
# Otherwise, we default to the local SQLite file 'students.db'.
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./students.db")

# 2. Create the Database Engine.
# The engine is the starting point for any SQLAlchemy application. It manages the connection pool.
# Note: 'connect_args={"check_same_thread": False}' is needed ONLY for SQLite.
# By default, SQLite only allows one thread to communicate with it, but FastAPI requests
# might be handled by multiple threads. This argument allows multi-threaded requests safely.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# 3. Create a Session Factory.
# SessionLocal is a factory class that will create database sessions for us.
# - autocommit=False: We want to manually control transaction commits (e.g., db.commit()).
# - autoflush=False: We do not want queries to automatically push changes to the database
#   until we explicitly request it.
# - bind=engine: Connects this session factory to our specific database engine created above.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Create the Declarative Base.
# This Base class is used to construct our database models.
# All our database tables (like Student) will inherit from this Base class so SQLAlchemy knows about them.
Base = declarative_base()


# 5. Database Session Dependency.
# This is a helper generator function that will create a new database session for each API request,
# yield it to the API endpoint, and ensure it is safely closed after the request is finished.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
