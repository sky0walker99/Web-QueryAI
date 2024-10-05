import asyncio
from crawl4ai import AsyncWebCrawler
from dotenv import load_dotenv
import os
import google.generativeai as genai
from abc import ABC, abstractmethod
from config import *
from models import *


# Load the API key from the .env file
load_dotenv()
genai.configure(api_key=os.environ["API_KEY"])


## Initialization of models
Web_QueryAi = AIModel(model_name ="gemini-1.5-pro" ,  generation_config = generation_config, system_instruction = system_instruction)

async def main():
    url = input("url : ")
    async with AsyncWebCrawler(verbose=True) as crawler:
        result = await crawler.arun(url)
        print(result.markdown)


def ai(url):
    pass

if __name__ == "__main__":
    asyncio.run(main())