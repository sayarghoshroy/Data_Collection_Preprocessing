# !pip install bs4
# !pip install lxml

import csv
import urllib
from urllib.request import urlopen, Request
import requests
from bs4 import BeautifulSoup
from requests_html import HTMLSession

csvfile = open('./output/in_book.csv', 'w', newline = '')

make_table = csv.writer(csvfile, delimiter = ';')

make_table.writerow(["Name", "URL", "Author", "Price",
                     "Number of Ratings", "Average Rating", "Type"])


def get_link(i):
    link = "https://www.amazon.in/gp/bestsellers/books/ref=zg_bs_pg" + str(i) + "?ie=UTF8&pg=" + str(i) + "&ajax=1"
    return link

agent = "Mozilla/5.0 (platform; rv:geckoversion) Gecko/geckotrail Firefox/firefoxversion"
# Reference: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/User-Agent

start = 1
limit = 10
view_url = True
view_count = True

for index in range(start, limit + 1):
    url = get_link(index)
    
    if view_url:
        print('URL: ' + url, flush = True)

    # Fetching the page

    # Option 1
    # page = requests.get(url)
    # html = page.text

    # Option 2
    # html = urllib.request.urlopen(url).read()
    # urllib is preferred for dynamic webpages but ...

    # Option 3
    try:
        html = urlopen(Request(url, headers = {'User-Agent': agent})).read()

    # Drawback: Will not scroll down to include all 50 items on a page
    # Workaround: Use selenium.webdriver to open the page and scroll down
    
    except Exception as E:
        print('Page ' + str(index) + ' Not Found', flush = True)
        continue

    soup = BeautifulSoup(html, 'lxml')

    # More Previously: books = soup.find_all('div', attrs = {"class": "zg_itemImmersion"})
    # Previously: books = soup.find_all('li', attrs = {"class": "zg-item-immersion"})
    books = soup.find_all('div', attrs = {"class": "zg-grid-general-faceout"})

    if view_count:
        print('Number of Books on page ' + str(index) + ' = ' + str(len(books)))
    
    for book in books:
        listed = []
        
        # name
        # Previously: setup = book.find("div", attrs = {"class": "p13n-sc-truncate p13n-sc-line-clamp-1"})
        setup = book.find("div", attrs = {"class": "_cDEzb_p13n-sc-css-line-clamp-1_1Fn1y"})

        if setup:
            listed.append((setup.text).strip())
        else:
            listed.append("not_available")
        
        # url
        setup = book.find("a", attrs={"class": "a-link-normal"})
        
        if setup:
            listed.append("https://www.amazon.in" + setup['href'])
        else:
            listed.append("not_available")
        
        # author
        setup = book.find("a", attrs = {"class": "a-size-small a-link-child"})

        # What about:
        # setup = book.find("div", attrs = {"class": "a-row a-size-small"})

        if setup:
            listed.append(setup.text)
        else:
            listed.append("not_available")
        
        # price
        # Previously: setup = book.find("span", attrs = {"class": "p13n-sc-price"})
        setup = book.find("span", attrs = {"class": "a-size-base a-color-price"})

        if setup:
            listed.append(setup.text.strip())
            # contains prefix u"\u20B9"
        else:
            listed.append("not_available")
        
        # number of ratings
        # Previously: setup = book.find("a", attrs = {"class": "a-size-small a-link-normal"})
        
        # Works with a few misses:
        # setup = book.find("span", attrs = {"class": "a-size-small"})

        # Better solution:
        # Pick the second last instance of the following match
        setup = book.find_all("span", attrs = {"class": "a-size-small"})[-2]
       
        if setup:
            listed.append((setup.text).strip())
        else:
            listed.append("not_available")
        
        # average rating
        setup = book.find("span", attrs = {"class": "a-icon-alt"})

        if setup and setup.text and (setup.text).strip() != "Prime":
            listed.append(setup.text)
        else:
            listed.append("not_available")


        # Type: Hardbound or paperback

        # Pick the last instance of the following match
        setup = book.find_all("span", attrs = {"class": "a-size-small"})[-1]

        if setup:
            listed.append((setup.text).strip())
        else:
            listed.append("not_available")
        
        make_table.writerow(listed)
