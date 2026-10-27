from scrapers.base_scraper import BaseScraper
from urllib.parse import quote

class LinkedInScraper(BaseScraper):
    def __init__(self, keywords='procurement', location='United States'):
        url = f'https://www.linkedin.com/jobs/search/?keywords={quote(keywords)}&location={quote(location)}'
        super().__init__('LinkedIn', url)
    
    def scrape(self):
        print(f"Scraping {self.name}...")
        html = self.fetch_page(self.url)
        if not html:
            return []
        
        soup = self.parse_html(html)
        jobs = []
        
        # LinkedIn job cards
        job_cards = soup.find_all('div', class_='base-card')
        
        for card in job_cards:
            try:
                title_elem = card.find('h3', class_='base-search-card__title')
                company_elem = card.find('h4', class_='base-search-card__subtitle')
                location_elem = card.find('span', class_='job-search-card__location')
                link_elem = card.find('a', class_='base-card__full-link')
                
                if title_elem and link_elem:
                    title = title_elem.get_text(strip=True)
                    company = company_elem.get_text(strip=True) if company_elem else 'N/A'
                    location = location_elem.get_text(strip=True) if location_elem else 'N/A'
                    job_url = link_elem.get('href', '')
                    
                    jobs.append({
                        'title': title,
                        'company': company,
                        'location': location,
                        'url': job_url,
                        'source': self.name
                    })
            except Exception as e:
                print(f"Error parsing job card: {e}")
                continue
        
        print(f"Found {len(jobs)} jobs from {self.name}")
        return jobs
