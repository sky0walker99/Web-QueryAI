import asyncio
from crawl4ai import AsyncWebCrawler
from dotenv import load_dotenv
import os
import google.generativeai as genai
from config import *
from models import *


# Load the API key from the .env file
load_dotenv()
genai.configure(api_key=os.environ["API_KEY"])


## Initialization of models
Web_QueryAi = AIModel(model_name ="gemini-1.5-pro" ,  generation_config = generation_config, system_instruction = system_instruction, )

async def main():
    url = input("url : ")
    initial_prompt = input("Prompt: ")
    
    #crawl and scrape the data using crawl4ai
    async with AsyncWebCrawler(verbose=True) as crawler:
        result = await crawler.arun(url)
    
    response = Web_QueryAi.get_response(result.markdown + "" + initial_prompt)
    print(f"response: {response}")
    
    while True:
        try:
            prompt = input("Prompt: ")
            response = Web_QueryAi.get_response(prompt)
            print(f"response: {response}\n")
            
        except KeyboardInterrupt:
            print("Shutting down gracefully...")
            break



    
if __name__ == "__main__":
    asyncio.run(main())
    
    