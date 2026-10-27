# 🤖 LinkedIn Job Scraper Agent

An intelligent automation tool that monitors LinkedIn for procurement and supply chain job postings, automatically extracts new listings, and sends email notifications.

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![Selenium](https://img.shields.io/badge/Selenium-4.15.0-green.svg)](https://www.selenium.dev/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## ✨ Features

- 🔐 **Automated LinkedIn Login** - Securely logs into your LinkedIn account
- 🔍 **Smart Job Search** - Searches for jobs based on customizable keywords
- 📜 **Infinite Scroll** - Automatically scrolls to load more job listings
- 💾 **Duplicate Prevention** - Saves only new jobs, avoiding duplicates
- 📧 **Email Notifications** - Sends alerts when new jobs are found
- ⏰ **Scheduled Runs** - Runs automatically at configurable intervals
- 📊 **Job Storage** - Saves all jobs to a JSON database for easy access

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Google Chrome browser
- Gmail account (for notifications)
- LinkedIn account

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/linkedin-job-scraper.git
cd linkedin-job-scraper
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure environment variables**

Copy the `.env.example` to `.env` and fill in your credentials:

```bash
cp .env.example .env
```

Edit `.env` with your information:
```env
# LinkedIn Credentials
LINKEDIN_EMAIL=your-email@example.com
LINKEDIN_PASSWORD=your-password

# Job Search Keywords
JOB_KEYWORDS=procurement,tender,bidding,contract,supply chain

# Email Notifications
ENABLE_EMAIL=true
EMAIL_TO=your-email@example.com
SMTP_USER=your-gmail@gmail.com
SMTP_PASSWORD=your-gmail-app-password

# Scraping Interval (hours)
SCRAPE_INTERVAL_HOURS=24
```

### 🔑 Gmail App Password Setup

For email notifications:
1. Enable 2-factor authentication on your Gmail account
2. Go to [Google App Passwords](https://myaccount.google.com/apppasswords)
3. Generate a new app password
4. Use this password in your `.env` file

## 📖 Usage

### Run the Agent

```bash
python run_agent.py
```

The agent will:
1. Open Chrome browser (visible)
2. Login to LinkedIn
3. Search for jobs matching your keywords
4. Scroll and extract job details
5. Save new jobs to `jobs.json`
6. Send email notification
7. Schedule next run in 24 hours

### View Saved Jobs

```bash
python view_jobs.py
```

### Test LinkedIn Connection

```bash
python test_linkedin.py
```

## 📁 Project Structure

```
procurement-job-agent/
├── agents/
│   ├── __init__.py
│   └── linkedin_agent.py      # Main scraping agent
├── config/
│   ├── __init__.py
│   └── settings.py            # Configuration loader
├── database/
│   ├── __init__.py
│   └── storage.py             # JSON database handler
├── notifications/
│   ├── __init__.py
│   └── email_notifier.py      # Email notification system
├── scrapers/
│   ├── __init__.py
│   └── base_scraper.py        # Base scraper class
├── .env                       # Environment variables (not in git)
├── .env.example               # Example env file
├── .gitignore                 # Git ignore rules
├── requirements.txt           # Python dependencies
├── run_agent.py               # Main entry point
├── view_jobs.py               # View saved jobs
├── test_linkedin.py           # Test script
└── README.md                  # This file
```

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `LINKEDIN_EMAIL` | Your LinkedIn email | Required |
| `LINKEDIN_PASSWORD` | Your LinkedIn password | Required |
| `JOB_KEYWORDS` | Comma-separated keywords | `procurement,supply chain` |
| `SCRAPE_INTERVAL_HOURS` | Hours between runs | `24` |
| `ENABLE_EMAIL` | Enable email notifications | `false` |
| `EMAIL_TO` | Recipient email address | - |
| `SMTP_SERVER` | SMTP server | `smtp.gmail.com` |
| `SMTP_PORT` | SMTP port | `587` |
| `SMTP_USER` | SMTP username | - |
| `SMTP_PASSWORD` | SMTP password/app password | - |

### Customizing Keywords

Edit the `JOB_KEYWORDS` in your `.env` file:

```env
JOB_KEYWORDS=procurement,supply chain,vendor management,sourcing,purchasing
```

## 🛡️ Security Best Practices

- ✅ Never commit `.env` file to version control
- ✅ Use Gmail App Password, not your main password
- ✅ Keep dependencies updated: `pip install --upgrade -r requirements.txt`
- ✅ LinkedIn may detect automation - use responsibly
- ✅ Consider using a separate LinkedIn account for scraping

## 🐛 Troubleshooting

### Browser doesn't open
- Make sure Chrome is installed
- Update Chrome to latest version
- Check if ChromeDriver is compatible with your Chrome version

### Login fails
- Verify credentials in `.env` file
- Check if LinkedIn requires additional verification
- Try running `test_linkedin.py` to debug

### No jobs found
- Check if keywords match actual job titles
- LinkedIn may be blocking automation (try with visible browser)
- Verify you're logged in successfully

### Email not sending
- Verify Gmail App Password is correct
- Check SMTP settings
- Ensure 2FA is enabled on Gmail

## 📊 Output Format

Jobs are saved in `jobs.json`:

```json
[
  {
    "title": "Procurement Manager",
    "company": "Example Corp",
    "location": "LinkedIn",
    "url": "https://www.linkedin.com/jobs/view/123456",
    "source": "LinkedIn Agent",
    "found_date": "2024-09-28T20:30:00"
  }
]
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This tool is for educational purposes only. Web scraping may violate LinkedIn's Terms of Service. Use at your own risk and respect rate limits. The authors are not responsible for any misuse or violations.

## 🙏 Acknowledgments

- Built with [Selenium](https://www.selenium.dev/)
- Inspired by the need for automated job hunting
- Thanks to the open-source community

## 📧 Contact

For questions or issues, please open an issue on GitHub.

---

**⭐ If you find this project helpful, please give it a star!**
