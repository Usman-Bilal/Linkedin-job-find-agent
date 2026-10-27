# Setup Guide

## Prerequisites

### Required Software
- **Python 3.8+**: Download from [python.org](https://www.python.org/downloads/)
- **Google Chrome**: Latest version recommended
- **Git**: For cloning the repository

### Required Accounts
- LinkedIn account
- Gmail account (for notifications)

## Step-by-Step Installation

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/linkedin-job-scraper.git
cd linkedin-job-scraper
```

### 2. Create Virtual Environment (Recommended)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

Copy the example environment file:
```bash
cp .env.example .env
```

Edit `.env` with your credentials:
```env
LINKEDIN_EMAIL=your-email@example.com
LINKEDIN_PASSWORD=your-secure-password
JOB_KEYWORDS=procurement,supply chain,sourcing
ENABLE_EMAIL=true
EMAIL_TO=alerts@example.com
SMTP_USER=your-gmail@gmail.com
SMTP_PASSWORD=your-app-password
```

### 5. Gmail App Password Setup

1. Go to your Google Account settings
2. Enable 2-Step Verification
3. Visit [App Passwords](https://myaccount.google.com/apppasswords)
4. Select "Mail" and "Windows Computer"
5. Generate password
6. Copy the 16-character password to `.env`

### 6. Test Setup

Run the test script:
```bash
python test_linkedin.py
```

Watch the browser open and verify login works.

### 7. Run the Agent

```bash
python run_agent.py
```

## Troubleshooting

### ChromeDriver Issues
If you see driver errors:
- Update Chrome to latest version
- Selenium will auto-download correct ChromeDriver

### Login Problems
- Verify credentials in `.env`
- Check for typos
- LinkedIn may require verification on first automated login

### Email Not Working
- Verify App Password (not regular password)
- Check SMTP settings
- Ensure 2FA is enabled

## Next Steps

- Customize job keywords in `.env`
- Adjust scraping interval
- Set up as background service (see DEPLOYMENT.md)
