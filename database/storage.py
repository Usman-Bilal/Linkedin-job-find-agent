import json
import os
from datetime import datetime

class JobStorage:
    def __init__(self, filename='jobs.json'):
        self.filename = filename
        self.jobs = self._load_jobs()
    
    def _load_jobs(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                return json.load(f)
        return []
    
    def save_job(self, job):
        if not self._job_exists(job['url']):
            job['found_date'] = datetime.now().isoformat()
            self.jobs.append(job)
            self._save_jobs()
            return True
        return False
    
    def _job_exists(self, url):
        return any(job['url'] == url for job in self.jobs)
    
    def _save_jobs(self):
        with open(self.filename, 'w') as f:
            json.dump(self.jobs, f, indent=2)
    
    def get_all_jobs(self):
        return self.jobs
    
    def get_recent_jobs(self, days=7):
        from datetime import timedelta
        cutoff = datetime.now() - timedelta(days=days)
        return [job for job in self.jobs 
                if datetime.fromisoformat(job['found_date']) > cutoff]
