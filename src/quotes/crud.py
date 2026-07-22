from datetime import datetime, date
from sqlalchemy import select, func
from src.db.database import async_session_factory
from src.quotes.models import Quote


# Inserts a new stock quote into the database
async def insert_quote(
    ticker: str,
    name: str,
    update_time: datetime,
    last_price: float,
    prev_price: float,
    change: float,
    change_percent: float,
    open_price: float,
    high: float,
    low: float,
    volume: int,
    value: float,
    lot_size: int,
):
    async with async_session_factory() as session:
        quote = Quote(
            ticker=ticker,
            name=name,
            update_time=update_time,
            last_price=last_price,
            prev_price=prev_price,
            change=change,
            change_percent=change_percent,
            open=open_price,
            high=high,
            low=low,
            volume=volume,
            value=value,
            lot_size=lot_size
        )

        session.add(quote)
        await session.commit()

        await session.refresh(quote)

        quote_id = quote.id

        return quote_id


# Fetch all stock quotes from the database
async def get_all_quotes():
    async with async_session_factory() as session:
        result = await session.execute(
            select(Quote).order_by(Quote.id.asc())
        )

        quotes = result.scalars().all()

        return [
            {
                "id": q.id,
                "update_time": q.update_time,
                "ticker": q.ticker,
                "name": q.name,
                "last_price": q.last_price,
                "prev_price": q.prev_price,
                "change": q.change,
                "change_percent": q.change_percent,
                "open": q.open,
                "high": q.high,
                "low": q.low,
                "volume": q.volume,
                "value": q.value,
                "lot_size": q.lot_size
            }
            for q in quotes
        ]


# Fetch all stock quotes from the database by date
async def get_quotes(
    start_date: date | None = None,
    end_date: date | None = None
):
    async with async_session_factory() as session:
        query = select(Quote).order_by(Quote.id.asc())

        if start_date is not None:
            query = query.where(
                func.date(Quote.update_time) >= start_date
            )

        if end_date is not None:
            query = query.where(
                func.date(Quote.update_time) <= end_date
            )

        result = await session.execute(query)
        quotes = result.scalars().all()

        return [
            {
                "id": q.id,
                "update_time": q.update_time,
                "ticker": q.ticker,
                "name": q.name,
                "last_price": q.last_price,
                "prev_price": q.prev_price,
                "change": q.change,
                "change_percent": q.change_percent,
                "open": q.open,
                "high": q.high,
                "low": q.low,
                "volume": q.volume,
                "value": q.value,
                "lot_size": q.lot_size
            }
            for q in quotes
        ]
