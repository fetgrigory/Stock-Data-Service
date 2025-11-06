'''
This module make

Author: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 06/11/2025
Ending //

'''
# Installing the necessary libraries
from sqlalchemy import Table, Column, Integer, String, MetaData
# Creating a metadata object to hold table definitions
metadata_obj = MetaData()
# Defining the 'users' table structure
users_table = Table(
    "users",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("username", String),
    Column("password", String),
)
