import os
from dotenv import load_dotenv

load_dotenv()

# Scraping settings
SCRAPE_INTERVAL_HOURS = int(os.getenv('SCRAPE_INTERVAL_HOURS', 24))
MAX_RETRIES = int(os.getenv('MAX_RETRIES', 3))
JOB_KEYWORDS = os.getenv('JOB_KEYWORDS', 'procurement').split(',')

# Email settings
ENABLE_EMAIL = os.getenv('ENABLE_EMAIL', 'false').lower() == 'true'
EMAIL_TO = os.getenv('EMAIL_TO', '')
SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
SMTP_USER = os.getenv('SMTP_USER', '')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD', '')

# Job sources
JOB_SOURCES = [
    {
        'name': 'Sample Job Board',
        'url': 'https://example.com/jobs',
        'enabled': True
    }
]
