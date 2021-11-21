# !pip install bs4
# !pip install lxml

import csv
import time
import json
import urllib
from urllib.request import urlopen, Request
import requests
from bs4 import BeautifulSoup
from requests_html import HTMLSession

csvfile = open('./output/phones.csv', 'w', newline='')

make_table = csv.writer(csvfile, delimiter = ';')

attribute_to_element = {
    "Announced": ["td", {"data-spec": "year"}],
    "Release Status": ["td", {"data-spec": "status"}],
    "Dimensions": ["td", {"data-spec": "dimensions"}],
    "Weight": ["td", {"data-spec": "weight"}],
    "Sim Type": ["td", {"data-spec": "sim"}],
    "Display Type": ["td", {"data-spec": "displaytype"}],
    "Display Size": ["td", {"data-spec": "displaysize"}],
    "Display Resolution": ["td", {"data-spec": "displayresolution"}],
    "Display Protection": ["td", {"data-spec": "displayprotection"}],
    "OS": ["td", {"data-spec": "os"}],
    "Chipset": ["td", {"data-spec": "chipset"}],
    "CPU": ["td", {"data-spec": "cpu"}],
    "GPU": ["td", {"data-spec": "gpu"}],
    "Internal Memory": ["td", {"data-spec": "memoryslot"}],
    "Memory Card Slot": ["td", {"data-spec": "internalmemory"}],
    "Main Camera Setup": ["td", {"data-spec": "cam1modules"}],
    "Main Camera Features": ["td", {"data-spec": "cam1features"}],
    "Main Camera Video Capabilities": ["td", {"data-spec": "cam1video"}],
    "Secondary Camera Setup": ["td", {"data-spec": "cam2modules"}],
    "Secondary Camera Features": ["td", {"data-spec": "cam2features"}],
    "Secondary Camera Video Capabilities": ["td", {"data-spec": "cam2video"}],
    "Loudspeaker": ["a", {"href": "glossary.php3?term=loudspeaker"}],
    "3.5mm Jack": ["a", {"href": "glossary.php3?term=audio-jack"}],
    "WLAN": ["td", {"data-spec": "wlan"}],
    "Bluetooth": ["td", {"data-spec": "bluetooth"}],
    "GPS": ["td", {"data-spec": "gps"}],
    "NFC": ["td", {"data-spec": "nfc"}],
    "Infrared Port": ["a", {"href": "glossary.php3?term=irda"}],
    "Radio": ["td", {"data-spec": "radio"}],
    "USB": ["td", {"data-spec": "usb"}],
    "Sensors": ["td", {"data-spec": "sensors"}],
    "Battery Type": ["td", {"data-spec": "batdescription1"}],
    "Battery Charging": ["a", {"href": "glossary.php3?term=battery-charging"}],
    "Colors": ["td", {"data-spec": "colors"}],
    "Price": ["td", {"data-spec": "price"}]
}

all_attributes = ["Name", "URL"]

for attribute in attribute_to_element.keys():
    all_attributes.append(attribute)

make_table.writerow(all_attributes)

test_out = False

if test_out:
    links = ['https://www.gsmarena.com/xiaomi_11_lite_5g_ne-11101.php', 'https://www.gsmarena.com/oneplus_nord_n200_5g-10961.php']
else:
    with open('crawled_URLs_2000.json', 'r+') as f:
        links = json.load(f)

    print('Number of raw URLs to look at: ' + str(len(links)))

agent = "Safari"
# Reference: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/User-Agent

view_url = True
view_count = True

def add_element(listed, item):
    if item:
        text = item.text.replace("\n", "")
        listed.append(text)
    else:
        listed.append("not_available")

    return listed

def handle_element(soup, element):
    
    field_a = element[0]
    field_b = element[1]

    if field_a == 'a':
        
        try:  
            # Case 2      
            child = soup.find(field_a, attrs = element[1])

            parent = child.parent.parent

            info_field = parent.find('td', attrs = {"class": "nfo"})
            return info_field

        except Exception as E:
            return None
    
    # Case 1
    return soup.find(field_a, attrs = element[1])

for url in links:
    time.sleep(1)
    
    if view_url:
        print('URL: ' + url, flush = True)

    try:
        html = urlopen(Request(url, headers = {'User-Agent': agent})).read()
        # html = requests.get(url).text
    
    except Exception as E:
        print(url + ' not found.', flush = True)
        continue

    soup = BeautifulSoup(html, 'lxml')

    listed = []
    
    # name
    setup = soup.find("h1", attrs = {"class": "specs-phone-name-title"})

    # Also checks if it is a valid page
    if setup:
        listed.append((setup.text).strip())
    else:
        # Not a valid page
        continue
    
    # url
    listed.append(url)

    for key in attribute_to_element.keys():

        element = attribute_to_element[key]
        setup = handle_element(soup, element)
        listed = add_element(listed, setup)
    
    make_table.writerow(listed)

# Try out: Using 'a' with 'href' based find() with sibling extraction for the other fields
# Combine get_data.py and crawl_phones.py into one crawling + scraping script
