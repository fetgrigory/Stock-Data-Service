'''
This module make

Author: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 25/09/2025
Ending //

'''
# Installing the necessary libraries
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from src.db.models import Base
# Loading variables from .env
load_dotenv()
# Getting variables from the environment
HOST = os.getenv("HOST")
DBNAME = os.getenv("DBNAME")
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
PORT = os.getenv("PORT")
# Creating a connection string
DATABASE_URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}"
# Creating an engine
engine = create_engine(
    DATABASE_URL,
    echo=False,
    pool_size=5,
    max_overflow=10
)
Base.metadata.bind = engine
