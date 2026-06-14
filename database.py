"""
database.py
============
Sets up the SQLAlchemy engine, session factory, and declarative Base
that all ORM models inherit from.

We use SQLite (a single file: cms.db) for zero-setup local development.
To switch to PostgreSQL or MySQL later, just change DATABASE_URL, e.g.:

    PostgreSQL: "postgresql://user:password@localhost/dbname"
    MySQL:      "mysql+pymysql://user:password@localhost/dbname"

and remove the SQLite-only `connect_args`.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLite database file, created automatically in the project root
DATABASE_URL = "sqlite:///./cms.db"

# `check_same_thread=False` is required only for SQLite, since FastAPI
# may use the connection from a different thread than it was created in.
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

# SessionLocal is a factory that creates new Session objects when called
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class that every ORM model (table) must inherit from
Base = declarative_base()


def get_db():
    """
    FastAPI dependency that yields a database session for a single
    request and guarantees it is closed afterwards, even if an
    exception occurs.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()