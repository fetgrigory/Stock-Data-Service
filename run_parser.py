import asyncio
import aiohttp
from src.scheduler import Scheduler
from src.parsing.data_parser import StockDataParser, MOEXApiWrapper


async def main():
    async with aiohttp.ClientSession() as session:
        api_wrapper = MOEXApiWrapper(session)
        parser = StockDataParser(api_wrapper)
        scheduler = Scheduler(parser=parser)

        await scheduler.start_schedule()


if __name__ == "__main__":
    asyncio.run(main())
