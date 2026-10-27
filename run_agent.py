#!/usr/bin/env python3
"""
LinkedIn Job Scraper Agent
Uses LangChain AI agent to intelligently scrape LinkedIn jobs
"""
import schedule
import time
from agents.linkedin_agent import LinkedInJobAgent
from database.storage import JobStorage
from notifications.email_notifier import EmailNotifier
from config.settings import SCRAPE_INTERVAL_HOURS, JOB_KEYWORDS
import os

def run_job_scraper():
    print("\n" + "="*70)
    print("🤖 LinkedIn Job Scraper Agent Started")
    print("="*70)
    
    # Initialize components
    agent = LinkedInJobAgent()
    storage = JobStorage()
    notifier = EmailNotifier()
    
    # Get keywords
    keywords = ','.join(JOB_KEYWORDS)
    print(f"🔍 Searching for: {keywords}\n")
    
    # Run the agent
    jobs = agent.run_manual_scrape(keywords)
    
    # Save new jobs
    if jobs:
        new_jobs = []
        for job in jobs:
            job['source'] = 'LinkedIn Agent'
            job['location'] = 'LinkedIn'
            
            if storage.save_job(job):
                new_jobs.append(job)
                print(f"✓ New job saved: {job['title']} at {job['company']}")
        
        print(f"\n📊 Total new jobs found: {len(new_jobs)}")
        
        # Send email notification
        if new_jobs:
            notifier.send_job_notification(new_jobs)
    else:
        print("⚠️ No jobs extracted")
    
    print("\n" + "="*70)
    print(f"✅ Scrape complete at {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70 + "\n")

def main():
    print("\n🚀 Starting LinkedIn Job Agent Scheduler")
    print(f"📅 Will run every {SCRAPE_INTERVAL_HOURS} hours")
    print("Press Ctrl+C to stop\n")
    
    # Run immediately
    run_job_scraper()
    
    # Schedule periodic runs
    schedule.every(SCRAPE_INTERVAL_HOURS).hours.do(run_job_scraper)
    
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Stopping LinkedIn Job Agent...")
        print("Goodbye!\n")
