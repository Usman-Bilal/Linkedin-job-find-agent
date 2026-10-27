from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from dotenv import load_dotenv

load_dotenv()

class LinkedInAuthScraper:
    def __init__(self, keywords='procurement', location='United States'):
        self.name = 'LinkedIn Jobs'
        self.keywords = keywords
        self.email = os.getenv('LINKEDIN_EMAIL', '')
        self.password = os.getenv('LINKEDIN_PASSWORD', '')
        
    def scrape(self):
        if not self.email or not self.password:
            print("❌ LinkedIn credentials missing in .env file")
            return []
        
        print(f"\n{'='*60}")
        print(f"🔍 Starting LinkedIn Job Search for: {self.keywords}")
        print(f"{'='*60}\n")
        
        options = Options()
        options.add_argument('--start-maximized')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        driver = None
        jobs = []
        
        try:
            print("🌐 Opening Chrome browser...")
            driver = webdriver.Chrome(options=options)
            wait = WebDriverWait(driver, 15)
            
            # Step 1: Login
            print("🔐 Logging into LinkedIn...")
            driver.get('https://www.linkedin.com/login')
            time.sleep(2)
            
            driver.find_element(By.ID, 'username').send_keys(self.email)
            time.sleep(0.5)
            driver.find_element(By.ID, 'password').send_keys(self.password)
            time.sleep(0.5)
            driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
            
            print("⏳ Waiting for login to complete...")
            time.sleep(8)
            
            # Check if login was successful
            current_url = driver.current_url
            if 'checkpoint' in current_url or 'challenge' in current_url:
                print("⚠️  Security verification required")
                print("Please complete verification manually in the browser")
                input("Press Enter after completing verification...")
            
            if 'login' in current_url:
                print("❌ Login failed - check your credentials")
                return []
            
            print("✅ Login successful!")
            
            # Step 2: Navigate to jobs
            print(f"\n🔎 Searching for '{self.keywords}' jobs...")
            jobs_url = f'https://www.linkedin.com/jobs/search/?keywords={self.keywords}'
            driver.get(jobs_url)
            time.sleep(4)
            
            # Step 3: Scroll to load more jobs
            print("📜 Scrolling to load job listings...")
            last_height = driver.execute_script("return document.body.scrollHeight")
            
            for scroll_num in range(5):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height
                print(f"  Scroll {scroll_num + 1}/5...")
            
            # Step 4: Extract job information
            print("\n📋 Extracting job details...")
            
            # Try multiple selectors
            job_selectors = [
                'li.jobs-search-results__list-item',
                'div.job-card-container',
                'div.base-card',
                'li[data-occludable-job-id]'
            ]
            
            job_elements = []
            for selector in job_selectors:
                job_elements = driver.find_elements(By.CSS_SELECTOR, selector)
                if job_elements:
                    print(f"✓ Found {len(job_elements)} jobs using selector: {selector}")
                    break
            
            if not job_elements:
                print("❌ No job elements found")
                print("💡 Try running with visible browser to debug")
                return []

            # Extract job details from each card
            for idx, element in enumerate(job_elements[:30], 1):
                try:
                    # Try different title selectors
                    title = None
                    title_selectors = ['h3.base-search-card__title', 'span.sr-only', 'h3', 'a[data-tracking-control-name]']
                    for ts in title_selectors:
                        try:
                            title = element.find_element(By.CSS_SELECTOR, ts).text.strip()
                            if title:
                                break
                        except:
                            continue
                    
                    # Try different company selectors
                    company = 'N/A'
                    company_selectors = ['h4.base-search-card__subtitle', 'a.hidden-nested-link', 'h4']
                    for cs in company_selectors:
                        try:
                            company = element.find_element(By.CSS_SELECTOR, cs).text.strip()
                            if company:
                                break
                        except:
                            continue
                    
                    # Get job URL
                    url = ''
                    try:
                        link_element = element.find_element(By.CSS_SELECTOR, 'a[href*="/jobs/"]')
                        url = link_element.get_attribute('href')
                    except:
                        try:
                            url = element.find_element(By.TAG_NAME, 'a').get_attribute('href')
                        except:
                            pass
                    
                    # Only add if we have title and URL
                    if title and url and len(title) > 3:
                        jobs.append({
                            'title': title,
                            'company': company,
                            'location': 'LinkedIn',
                            'url': url.split('?')[0],  # Clean URL
                            'source': self.name
                        })
                        print(f"  {idx}. ✓ {title} - {company}")
                    
                except Exception as e:
                    continue
            
            print(f"\n{'='*60}")
            print(f"✅ Successfully extracted {len(jobs)} jobs!")
            print(f"{'='*60}\n")
            
            # Keep browser open for 5 seconds to see results
            time.sleep(5)
            
            return jobs
            
        except Exception as e:
            print(f"\n❌ Error occurred: {e}")
            import traceback
            traceback.print_exc()
            return []
            
        finally:
            if driver:
                driver.quit()
                print("🔒 Browser closed")
