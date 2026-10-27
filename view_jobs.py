from database.storage import JobStorage
from datetime import datetime

def view_jobs():
    storage = JobStorage()
    jobs = storage.get_all_jobs()
    
    if not jobs:
        print("No jobs found yet. Run main.py to start scraping.")
        return
    
    print(f"\n{'='*80}")
    print(f"Total Jobs Found: {len(jobs)}")
    print(f"{'='*80}\n")
    
    for i, job in enumerate(jobs, 1):
        print(f"{i}. {job['title']}")
        print(f"   Company: {job['company']}")
        print(f"   Location: {job.get('location', 'N/A')}")
        print(f"   Source: {job['source']}")
        print(f"   URL: {job['url']}")
        print(f"   Found: {job['found_date']}")
        print()

if __name__ == "__main__":
    view_jobs()
