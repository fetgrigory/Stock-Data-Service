'''
This module make

Author: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 06/11/2025
Ending //

'''
# Installing the necessary libraries
from sqlalchemy import Integer, Numeric, String, Text, BigInteger, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


# Creating a base class for models
class Base(DeclarativeBase):
    pass


# Defining the 'users' table structure
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, nullable=False, autoincrement=True)
    username: Mapped[str] = mapped_column(Text, nullable=False)
    email: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    password: Mapped[str] = mapped_column(Text, nullable=False)


# Defining the 'recipients' table structure
class Recipient(Base):
    __tablename__ = "recipients"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    email: Mapped[str] = mapped_column(Text, nullable=False)


# Defining the 'smtp_settings' table structure
class SmtpSetting(Base):
    __tablename__ = "smtp_settings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, nullable=False, autoincrement=True)
    server: Mapped[str] = mapped_column(Text, nullable=False)
    port: Mapped[int] = mapped_column(Integer, nullable=False)
    username: Mapped[str] = mapped_column(Text, nullable=False)
    password: Mapped[str] = mapped_column(Text, nullable=False)
    sender: Mapped[str] = mapped_column(Text, nullable=False)


# Defining the 'quotes' table structure
class Quote(Base):
    __tablename__ = "quotes"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    ticker: Mapped[str] = mapped_column(String(20), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    last_price: Mapped[float] = mapped_column(Numeric(20, 4))
    prev_price: Mapped[float] = mapped_column(Numeric(20, 4))
    change: Mapped[float] = mapped_column(Numeric(20, 4))
    change_percent: Mapped[float] = mapped_column(Numeric(20, 4))
    open: Mapped[float] = mapped_column(Numeric(20, 4))
    high: Mapped[float] = mapped_column(Numeric(20, 4))
    low: Mapped[float] = mapped_column(Numeric(20, 4))
    volume: Mapped[int] = mapped_column(BigInteger)
    value: Mapped[float] = mapped_column(Numeric(20, 2))
    update_time: Mapped[DateTime] = mapped_column(nullable=False)
    lot_size: Mapped[int] = mapped_column(BigInteger)
