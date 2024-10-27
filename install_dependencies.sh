#!/bin/bash



# Download Google Chrome
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb

# Install Google Chrome
sudo apt install -y ./google-chrome-stable_current_amd64.deb

# Change to the src directory
cd src

# Run the Streamlit application
streamlit run app.py
