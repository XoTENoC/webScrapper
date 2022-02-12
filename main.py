from tkinter.font import names
from unicodedata import name
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.select import Select
from bs4 import BeautifulSoup

import os
import re
import time
import pandas as pd

# Function for making sure that the website has loaded before continuing
def wait_for_page_load():
    timer = 10
    start_time = time.time()
    page_state = None
    while page_state != 'complete':
        time.sleep(0.5)
        page_state = Browser.execute_script('return document.readyState;')
        if time.time() - start_time > timer:
            raise Exception('Timeout :(')

# Defining the Webdriver to use
Browser = webdriver.Chrome()

# Definging the website to scrap
Browser.get("https://gpex.com.au/connect/training-regions/flinders-mid-north/")

# Text to search
links = Browser.find_elements(By.CSS_SELECTOR, "div.practice_list ul li a")

# init arrays
hrefs = []
names = []
numberOfDoc = []

# Assigning all the links to array
for link in links:
    hrefs.append(link.get_attribute("href"))
    names.append(link.text)

# Searching through all the links for the information
for href in hrefs:
    Browser.get(href)
    wait_for_page_load()

    # checking to make sure that the information is there
    try:
        no_docs = Browser.find_element(By.CLASS_NAME, "practice_number_of_doctors").get_attribute('innerHTML')
    except:
        no_docs = "Number of doctors: 0"
        
    numberOfDoc.append(no_docs)

# Closing the browser
Browser.close()

# Exporting the data to csv
df = pd.DataFrame({"Name of Practice" : names, "Number of Doctors" : numberOfDoc})
df.to_csv("flinders_mid_north.csv", index=False)
