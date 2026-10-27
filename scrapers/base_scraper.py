from abc import ABC, abstractmethod
import requests
from bs4 import BeautifulSoup

class BaseScraper(ABC):
    def __init__(self, name, url):
        self.name = name
        self.url = url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    @abstractmethod
    def scrape(self):
        pass
    
    def fetch_page(self, url):
        try:
            response = requests.get(url, headers=self.headers, timeout=30)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None
    
    def parse_html(self, html):
        return BeautifulSoup(html, 'html.parser')
    
    def extract_jobs(self, soup, keywords):
        jobs = []
        # Override this method in child classes
        return jobs
