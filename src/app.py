import sys
import os
from config import *
from models import *
from crawler import *
import pprint
import google.generativeai as genai
import asyncio
from crawl4ai import AsyncWebCrawler
from dotenv import load_dotenv
import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from playwright.async_api import async_playwright
# Load the API key from the .env file
load_dotenv()
genai.configure(api_key=os.environ["API_KEY"])

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

if "url_analyzed" not in st.session_state:
    st.session_state.url_analyzed = False

def main(url, prompt, model):    
    try:    
        Web_QueryAi = AIModel(
            model_name=model,
            generation_config=generation_config,
            system_instruction=system_instruction,
        )

        if not st.session_state.url_analyzed:
            crawler = WebCrawler(verbose=True)
            result = crawler.run(url)
            st.session_state.crawled_content = result
            st.session_state.url_analyzed = True

        response = Web_QueryAi.get_response(
            st.session_state.crawled_content + "\n" + prompt
        )
        return response
    except Exception as e:
        print(f"Error in main function: {e}")
        raise

# Streamlit UI
st.set_page_config(page_title="Web-QueryAI", layout="wide", initial_sidebar_state="expanded")

# Sidebar configuration
with st.sidebar:
    st.title("Settings")
    model = st.selectbox(
        "Choose a model:",
        ["gemini-1.5-flash", "gemini-1.5-pro"],
        key="model_select"
    )
    
    with st.expander("Advanced Settings"):
        system_instruction = st.text_area(
            "System Instructions:",
            "Provide relevant instructions for the AI model...",
            key="system_instructions"
        )
    
    st.title("Chat History")
    for message in st.session_state.messages:
        st.markdown(f"**{message['role'].capitalize()}:** {message['content']}")  # Display chat history

# Main content area
st.title("Web-QueryAI")

# URL input section
url_col1, url_col2 = st.columns([4, 1])
with url_col1:
    url = st.text_input("Enter a URL:", placeholder="https://example.com", key="url_input")
with url_col2:
    if st.button("Analyze Page", key="analyze_btn"):
        if url:
            with st.spinner("Analyzing webpage..."):
                st.session_state.url_analyzed = False
                try:
                    # Reset the chat when analyzing a new URL
                    st.session_state.messages = []
                    main(url=url, prompt="Summarize this page briefly", model=model)
                    st.success("Page analyzed successfully!")
                except Exception as e:
                    st.error(f"Error analyzing page: {str(e)}")

# Chat interface
st.divider()
chat_container = st.container()

# Display chat history
with chat_container:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User input
    if prompt := st.chat_input("Ask about the page...", key="chat_input"):
        if not url or not st.session_state.url_analyzed:
            st.error("Please enter a URL and analyze the page first.")
        else:
            # Add user message to chat
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # Get AI response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    try:
                        response = main(url=url, prompt=prompt, model=model)
                        st.markdown(response)
                        # Add assistant response to chat
                        st.session_state.messages.append(
                            {"role": "assistant", "content": response}
                        )
                    except Exception as e:
                        st.error(f"Error: {str(e)}")

# Clear chat button
if st.sidebar.button("Clear Chat", key="clear_chat"):
    st.session_state.messages = []
    st.session_state.url_analyzed = False
    st.rerun()
    

