import asyncio
import logging

from src.workers.scheduler.services.deps import provide_scheduler


async def run():
    logging.basicConfig(level=logging.INFO)
    scheduler = await provide_scheduler(logger=logging.getLogger(__name__))
    scheduler.scheduler.start()

    try:
        done = asyncio.Event()
        await done.wait()
    finally:
        scheduler.scheduler.shutdown()


if __name__ == "__main__":
    asyncio.run(run())
