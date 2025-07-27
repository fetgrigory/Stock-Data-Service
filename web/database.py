'''
This module make

Author: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 27/07/2025
Ending //

'''
# Installing the necessary libraries
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# Database configuration
DATABASE_URL = "sqlite:///./users.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """AI is creating summary for get_db

    Yields:
        [type]: [description]
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
