# !pip install bs4
# !pip install lxml

import csv
import urllib
from urllib.request import urlopen, Request
import requests
from bs4 import BeautifulSoup
from requests_html import HTMLSession

csvfile = open('./output/in_book.csv', 'w', newline = '')

make_table = csv.writer(csvfile, delimiter = ';',
                        quotechar = '|', quoting = csv.QUOTE_MINIMAL)

make_table.writerow(["Name", "URL", "Author", "Price",
                     "Number of Ratings", "Average Rating"])


def get_link(i):
    link = "https://www.amazon.in/gp/bestsellers/books/ref=zg_bs_pg" + str(i) + "?ie=UTF8&pg=" + str(i) + "&ajax=1"
    return link

agent = "Mozilla/5.0 (platform; rv:geckoversion) Gecko/geckotrail Firefox/firefoxversion"
# Reference: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/User-Agent

start = 1
limit = 3
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
    
    except Exception as E:
        print('Page ' + str(index) + ' Not Found', flush = True)
        continue

    soup = BeautifulSoup(html, 'lxml')

    # Previously: books = soup.find_all('div', attrs = {"class": "zg_itemImmersion"})
    books = soup.find_all('li', attrs = {"class": "zg-item-immersion"})

    if view_count:
        print('Number of Books on page ' + str(index) + ' = ' + str(len(books)))
    
    for book in books:
        listed = []
        
        # name
        setup = book.find("div", attrs = {"class": "p13n-sc-truncate p13n-sc-line-clamp-1"})
        
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
        setup = book.find("span", attrs = {"class": "p13n-sc-price"})
        
        if setup:
            listed.append(setup.text.strip())
            # contains prefix u"\u20B9"
        else:
            listed.append("not_available")
        
        # number of ratings
        setup = book.find("a", attrs = {"class": "a-size-small a-link-normal"})
       
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
        
        make_table.writerow(listed)
