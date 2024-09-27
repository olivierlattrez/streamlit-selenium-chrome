import streamlit as st
from scraper import google_search
"""
## Web scraping on Streamlit Cloud with Selenium

[![Source](https://img.shields.io/badge/View-Source-<COLOR>.svg)](https://github.com/snehankekre/streamlit-selenium-chrome/)

This is a minimal, reproducible example of how to scrape the web with Selenium and Chrome on Streamlit's Community Cloud.

Fork this repo, and edit `/streamlit_app.py` to customize this app to your heart's desire. :heart:
"""

#with st.echo():
    # from selenium import webdriver
    # from selenium.webdriver.chrome.options import Options
    # from selenium.webdriver.chrome.service import Service
    # from webdriver_manager.chrome import ChromeDriverManager
    # from webdriver_manager.core.os_manager import ChromeType

# @st.cache_resource
    # def get_driver():
    #     return webdriver.Chrome(
    #         service=Service(
    #             ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()
    #         ),
    #         options=options,
    #     )

    # options = Options()
    # options.add_argument("--disable-gpu")
    # options.add_argument("--headless")
    #
    # driver = get_driver()
    # driver.get("http://example.com")

    #st.code(driver.page_source)

# Title of the app
st.title("Simple Email and Phone Number Input App")

# Create input fields for email and phone number
email = st.text_input("Enter your Name:")
phone = st.text_input("Enter your phone number:")

print(google_search(email))
