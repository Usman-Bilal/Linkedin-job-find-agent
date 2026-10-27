from scrapers.base_scraper import BaseScraper
from urllib.parse import quote
import time

class IndeedScraper(BaseScraper):
    def __init__(self, location='United States'):
        url = f'https://www.indeed.com/jobs?q=procurement&l={quote(location)}'
        super().__init__('Indeed', url)
        # Better headers to avoid 403
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
    
    def scrape(self):
        print(f"Scraping {self.name}...")
        time.sleep(2)  # Add delay
        html = self.fetch_page(self.url)
        if not html:
            return []
        
        soup = self.parse_html(html)
        jobs = []
        
        # Indeed job cards - multiple possible selectors
        job_cards = soup.find_all('div', class_='job_seen_beacon') or \
                    soup.find_all('div', class_='jobsearch-SerpJobCard') or \
                    soup.find_all('a', class_='jcs-JobTitle')
        
        for card in job_cards[:15]:
            try:
                if card.name == 'a':
                    title = card.get_text(strip=True)
                    job_url = 'https://www.indeed.com' + card.get('href', '')
                    company = 'N/A'
                else:
                    title_elem = card.find('h2') or card.find('a', class_='jcs-JobTitle')
                    company_elem = card.find('span', attrs={'data-testid': 'company-name'})
                    
                    if not title_elem:
                        continue
                        
                    title = title_elem.get_text(strip=True)
                    company = company_elem.get_text(strip=True) if company_elem else 'N/A'
                    link = card.find('a')
                    job_url = 'https://www.indeed.com' + link.get('href', '') if link else ''
                
                if title and job_url:
                    jobs.append({
                        'title': title,
                        'company': company,
                        'location': 'United States',
                        'url': job_url,
                        'source': self.name
                    })
            except Exception as e:
                continue
        
        print(f"Found {len(jobs)} jobs from {self.name}")
        return jobs
