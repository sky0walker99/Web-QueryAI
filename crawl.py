import asyncio
from crawl4ai import *

async def main():
    url = input("url: ")
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url=url)
        print(result.markdown)
        return str(result.markdown)

if __name__ == "__main__":
    output = asyncio.run(main())
    with open("crawled.txt", "a+", encoding="utf-8") as f:
        f.write(output + "\n")
