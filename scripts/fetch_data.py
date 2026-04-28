import httpx
import asyncio


async def fetch_legislation():
    print("Fetching legislation...")


async def fetch_news():
    print("Fetching news...")


async def fetch_events():
    print("Fetching events...")


async def main():
    await fetch_legislation()
    await fetch_news()
    await fetch_events()


if __name__ == "__main__":
    asyncio.run(main())
