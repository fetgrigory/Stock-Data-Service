import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.db.models import Base
# Loading variables from .env
load_dotenv()
# Getting variables from the environment
DB_HOST = os.getenv("DB_HOST")
DBNAME = os.getenv("DBNAME")
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
PORT = os.getenv("PORT")
# Creating a connection string
DATABASE_URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@{DB_HOST}:{PORT}/{DBNAME}"
# Creating an engine
sync_engine = create_engine(
    DATABASE_URL,
    echo=False,
    pool_size=5,
    max_overflow=10
)
# Session factory
session_factory = sessionmaker(
    bind=sync_engine,
    autoflush=False,
    autocommit=False

)


# Creates all tables if they do not exist
def init_db():
    """AI is creating summary for init_db
    """
    Base.metadata.create_all(bind=sync_engine)
