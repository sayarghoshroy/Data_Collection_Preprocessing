import logging
import time
import json
from urllib.parse import urljoin
from url_normalize import url_normalize
import requests
from bs4 import BeautifulSoup

logging.basicConfig(format = '%(asctime)s %(levelname)s:%(message)s', level = logging.INFO)

class Crawler:

    def __init__(self, urls = [], domains = [], limit = 50):
        
        self.visited_urls = []
        self.urls_to_visit = urls
        self.limit = limit
        self.domains = domains
        return

    def download_url(self, url):
        try:
            time.sleep(1)
            return requests.get(url).text
        
        except Exception as E:
            return ''


    def get_linked_urls(self, url, html):
        soup = BeautifulSoup(html, 'html.parser')
        
        for link in soup.find_all('a'):
            
            path = link.get('href')

            #search.php3
            
            if path and (path.startswith('/') or not path.startswith('https://')):
                path = urljoin(url, path)

            yield path

    def domain_check(self, url):
        for domain in self.domains:
            if domain in url:
                return True
        return False

    def add_url_to_visit(self, url):
        total_crawled = len(self.visited_urls) + len(self.urls_to_visit)
        
        if total_crawled >= self.limit:
            return
        
        if not url or url == '':
            return

        if self.domain_check(url) == False:
            return

        if url not in self.visited_urls and url not in self.urls_to_visit:
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

    crawler = Crawler(urls = ['https://www.gsmarena.com/'], domains = ['https://www.gsmarena.com/'], limit = 2000)
    crawler.run()

    display = False
    
    if display == True:
        print(crawler.visited_urls, flush = True)

    # Saving visited URLs
    with open('crawled_URLs.json', 'w+') as f:
        json.dump(crawler.visited_urls, f)