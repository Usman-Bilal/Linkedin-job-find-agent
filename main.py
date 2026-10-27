import schedule
import time
from config.settings import SCRAPE_INTERVAL_HOURS, JOB_KEYWORDS
from database.storage import JobStorage
from scrapers.linkedin_selenium import LinkedInAuthScraper
from notifications.email_notifier import EmailNotifier

def run_scraper():
    print(f"\n=== Starting scrape job at {time.strftime('%Y-%m-%d %H:%M:%S')} ===")
    storage = JobStorage()
    notifier = EmailNotifier()
    
    # LinkedIn scraper only
    scrapers = [
        LinkedInAuthScraper(keywords='procurement', location='United States')
    ]
    
    total_new_jobs = 0
    new_jobs = []
    for scraper in scrapers:
        try:
            jobs = scraper.scrape()
            for job in jobs:
                if storage.save_job(job):
                    total_new_jobs += 1
                    new_jobs.append(job)
                    print(f"✓ New job: {job['title']} at {job['company']}")
        except Exception as e:
            print(f"Error with {scraper.name}: {e}")
    
    # Send email notification if new jobs found
    if new_jobs:
        notifier.send_job_notification(new_jobs)
    
    print(f"=== Scrape complete. {total_new_jobs} new jobs found ===\n")

def main():
    print("Procurement Job Agent Started")
    print(f"Searching for keywords: {', '.join(JOB_KEYWORDS)}")
    print(f"Scraping interval: {SCRAPE_INTERVAL_HOURS} hours\n")
    
    # Run once immediately
    run_scraper()
    
    # Schedule periodic runs
    schedule.every(SCRAPE_INTERVAL_HOURS).hours.do(run_scraper)
    
    print("Scheduler started. Press Ctrl+C to stop.")
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nStopping Procurement Job Agent...")
