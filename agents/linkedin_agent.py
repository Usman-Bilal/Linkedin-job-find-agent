from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import os
from dotenv import load_dotenv

load_dotenv()

class LinkedInJobAgent:
    def __init__(self):
        self.email = os.getenv('LINKEDIN_EMAIL', '')
        self.password = os.getenv('LINKEDIN_PASSWORD', '')
        self.driver = None
        
    def setup_browser(self):
        options = Options()
        options.add_argument('--start-maximized')
        options.add_argument('--disable-blink-features=AutomationControlled')
        self.driver = webdriver.Chrome(options=options)
        return "✅ Browser started"
    
    def login_linkedin(self):
        try:
            self.driver.get('https://www.linkedin.com/login')
            time.sleep(3)
            self.driver.find_element(By.ID, 'username').send_keys(self.email)
            self.driver.find_element(By.ID, 'password').send_keys(self.password)
            self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
            time.sleep(8)
            
            if 'feed' in self.driver.current_url or 'mynetwork' in self.driver.current_url:
                return "✅ Login successful"
            return "⚠️ Login may have failed"
        except Exception as e:
            return f"❌ Login error: {e}"
    
    def search_jobs(self, keywords):
        try:
            url = f'https://www.linkedin.com/jobs/search/?keywords={keywords}'
            self.driver.get(url)
            time.sleep(5)
            return f"✅ Searching for: {keywords}"
        except Exception as e:
            return f"❌ Search error: {e}"
    
    def scroll_page(self, times=5):
        try:
            for i in range(times):
                self.driver.execute_script("window.scrollBy(0, 800)")
                time.sleep(2)
            return f"✅ Scrolled {times} times"
        except Exception as e:
            return f"❌ Scroll error: {e}"

    def extract_jobs(self):
        try:
            jobs = []
            selectors = ['li.jobs-search-results__list-item', 'div.job-card-container', 'div.base-card']
            
            job_elements = []
            for selector in selectors:
                job_elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                if job_elements:
                    break
            
            for element in job_elements[:25]:
                try:
                    title = element.find_element(By.CSS_SELECTOR, 'h3, span.sr-only').text.strip()
                    company = element.find_element(By.CSS_SELECTOR, 'h4, a').text.strip()
                    url = element.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
                    
                    if title and url:
                        jobs.append({'title': title, 'company': company, 'url': url.split('?')[0]})
                except:
                    continue
            
            return f"✅ Extracted {len(jobs)} jobs: {jobs}"
        except Exception as e:
            return f"❌ Extraction error: {e}"
    
    def close_browser(self):
        if self.driver:
            self.driver.quit()
            return "✅ Browser closed"
        return "⚠️ No browser to close"
    
    def run_manual_scrape(self, keywords='procurement'):
        print("\n🤖 LinkedIn Job Scraper Agent\n")
        jobs = []
        try:
            print("1. " + self.setup_browser())
            print("2. " + self.login_linkedin())
            print("3. " + self.search_jobs(keywords))
            print("4. " + self.scroll_page(5))
            result = self.extract_jobs()
            print("5. " + result)
            
            if "Extracted" in result and "[" in result:
                import ast
                jobs_str = result.split(": ", 1)[1]
                jobs = ast.literal_eval(jobs_str)
            
            print("6. " + self.close_browser())
        except Exception as e:
            print(f"❌ Error: {e}")
            self.close_browser()
        
        return jobs
