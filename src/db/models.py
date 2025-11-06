'''
This module make

Author: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 06/11/2025
Ending //

'''
# Installing the necessary libraries
from sqlalchemy import Table, Column, Integer, Text, MetaData
# Creating a metadata object to hold table definitions
metadata_obj = MetaData()
# Defining the 'users' table structure
users_table = Table(
    "users",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("username", Text),
    Column("password", Text),
)
# Defining the 'recipients' table structure
recipients_table = Table(
    "recipients",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("name", Text),
    Column("email", Text),
)

# Defining the 'smtp_settings' table structure
smtp_settings_table = Table(
    "smtp_settings",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("server", Text),
    Column("port", Integer),
    Column("username", Text),
    Column("password", Text),
    Column("sender", Text),
)
