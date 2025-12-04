'''
This module make

Author: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 06/11/2025
Ending //

'''
# Installing the necessary libraries
from sqlalchemy import Integer, Numeric, String, Text, BigInteger
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


# Creating a base class for models
class Base(DeclarativeBase):
    pass


# Defining the 'users' table structure
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(Text, nullable=False)
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

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    ticker: Mapped[str] = mapped_column(String(20), nullable=False)
    trade_time: Mapped[str] = mapped_column(String(20), nullable=False)
    last_price: Mapped[float] = mapped_column(Numeric(12, 4), nullable=False)
    change_abs: Mapped[float] = mapped_column(Numeric(12, 4))
    change_percent: Mapped[float] = mapped_column(Numeric(20, 4))
    price_before_closing: Mapped[float] = mapped_column(Numeric(12, 4))
    price_at_opening: Mapped[float] = mapped_column(Numeric(12, 4))
    minimum_price: Mapped[float] = mapped_column(Numeric(12, 4))
    average_overpriced: Mapped[float] = mapped_column(Numeric(12, 4))
    pieces_per_day: Mapped[float] = mapped_column(Numeric(12, 4))
    quantity_per_day: Mapped[int] = mapped_column(BigInteger)
    rub: Mapped[float] = mapped_column(Numeric(15, 2))
    num_transactions_per_day: Mapped[int] = mapped_column(Integer)
