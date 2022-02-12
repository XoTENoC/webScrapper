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


def wait_for_page_load():
    timer = 10
    start_time = time.time()
    page_state = None
    while page_state != 'complete':
        time.sleep(0.5)
        page_state = Browser.execute_script('return document.readyState;')
        if time.time() - start_time > timer:
            raise Exception('Timeout :(')


Browser = webdriver.Chrome()

Browser.get("https://gpex.com.au/connect/training-regions/flinders-mid-north/")


links = Browser.find_elements(By.CSS_SELECTOR, "div.practice_list ul li a")

hrefs = []
names = []
numberOfDoc = []


for link in links:
    hrefs.append(link.get_attribute("href"))
    names.append(link.text)

hrefs2 = {}

for href in hrefs:
    hrefs2[href] = []
    Browser.get(href)
    wait_for_page_load()
    try:
        no_docs = Browser.find_element(By.CLASS_NAME, "practice_number_of_doctors").get_attribute('innerHTML')
    except:
        no_docs = "Number of doctors: 0"
        
    numberOfDoc.append(no_docs)

Browser.close()

df = pd.DataFrame({"Name of Practice" : names, "Number of Doctors" : numberOfDoc})
df.to_csv("flinders_mid_north.csv", index=False)
