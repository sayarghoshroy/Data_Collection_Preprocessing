import requests
import sys
import json

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC

url = "http://www.dashboard-padmaawards.gov.in/"
wait_time = 30 # wait-time in seconds

try:
	driver = webdriver.Chrome()
	driver.get(url)
	driver.execute_script("document.body.style.zoom='40%'")
	wait = WebDriverWait(driver, wait_time)
	response = driver.page_source

except Exception as E:
    print('Page Not Found.', flush = True)
    sys.exit(1)

soup = BeautifulSoup(response, 'lxml')

document = soup.find_all("div", attrs = {"class": "document"}) 
view_catalog =  soup.find_all("div", attrs = {"class": "view-catalog"}) 
awards_list = soup.find_all("div", attrs = {"class": "awards-list"}) 

view = True

if view:
	print(document)
	print(view_catalog)
	print(awards_list)
