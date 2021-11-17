import logging
import json
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

logging.basicConfig(format = '%(asctime)s %(levelname)s:%(message)s', level = logging.INFO)

class Crawler:

    def __init__(self, urls = [], limit = 50):
        
        self.visited_urls = []
        self.urls_to_visit = urls
        self.limit = limit
        return

    def download_url(self, url):
        try:
            return requests.get(url).text
        
        except Exception as E:
            return ''

    def get_linked_urls(self, url, html):
        soup = BeautifulSoup(html, 'html.parser')
        
        for link in soup.find_all('a'):
            
            path = link.get('href')
            
            if path and path.startswith('/'):
                path = urljoin(url, path)
            
            yield path

    def add_url_to_visit(self, url):
        total_crawled = len(self.visited_urls) + len(self.urls_to_visit)
        if total_crawled >= self.limit:
            return
        
        if url and url not in self.visited_urls and url not in self.urls_to_visit:
            # Why the if url?
            self.urls_to_visit.append(url)
            return

    def crawl(self, url):
        html = self.download_url(url)
        
        for url in self.get_linked_urls(url, html):
            self.add_url_to_visit(url)

    def run(self):
        while self.urls_to_visit:
            url = self.urls_to_visit.pop(0)
            
            logging.info(f' Fetching {url}')
            
            try:
                self.crawl(url)
            
            except Exception:
                logging.exception(f' Failed to fetch {url}')
            
            finally:
                self.visited_urls.append(url)

if __name__ == '__main__':

    crawler = Crawler(urls = ['https://www.imdb.com/'])
    crawler.run()

    display = False
    
    if display == True:
        print(crawler.visited_urls, flush = True)

    # Saving visited URLs
    with open('crawled_URLs.json', 'w+') as f:
        json.dump(crawler.visited_urls, f)

# No parallelism
# No retry mechanism
# No URL normalization ~ Homework: Find a python library function that does 'URL normalization'
# Ignores Robots.txt file