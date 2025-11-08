'''
This module make

Author: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 06/11/2025
Ending //

'''
# Installing the necessary libraries
from sqlalchemy import Column, Integer, Text
from sqlalchemy.orm import DeclarativeBase


# Creating a base class for models
class Base(DeclarativeBase):
    pass


# Defining the 'users' table structure
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(Text, nullable=False)
    password = Column(Text, nullable=False)


# Defining the 'recipients' table structure
class Recipient(Base):
    __tablename__ = "recipients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, nullable=False)
    email = Column(Text, nullable=False)


# Defining the 'smtp_settings' table structure
class SmtpSetting(Base):
    __tablename__ = "smtp_settings"

    id = Column(Integer, primary_key=True, index=True)
    server = Column(Text, nullable=False)
    port = Column(Integer, nullable=False)
    username = Column(Text, nullable=False)
    password = Column(Text, nullable=False)
    sender = Column(Text, nullable=False)
