from datetime import datetime
from sqlalchemy import Numeric, String,  BigInteger, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from src.db.base import Base


# Defining the 'quotes' table structure
class Quote(Base):
    __tablename__ = "quotes"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    update_time: Mapped[datetime] = mapped_column(DateTime, index=True, nullable=False)
    ticker: Mapped[str] = mapped_column(String(20), index=True, nullable=False)
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
    lot_size: Mapped[int] = mapped_column(BigInteger)
