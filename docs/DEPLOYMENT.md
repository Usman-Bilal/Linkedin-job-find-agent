# Deployment Guide

## Running as Background Service

### Option 1: Screen/Tmux (Linux/macOS)

**Using Screen:**
```bash
screen -S job-scraper
python run_agent.py
# Press Ctrl+A, then D to detach
# Reattach with: screen -r job-scraper
```

**Using Tmux:**
```bash
tmux new -s job-scraper
python run_agent.py
# Press Ctrl+B, then D to detach
# Reattach with: tmux attach -t job-scraper
```

### Option 2: Systemd Service (Linux)

Create service file: `/etc/systemd/system/job-scraper.service`

```ini
[Unit]
Description=LinkedIn Job Scraper Agent
After=network.target

[Service]
Type=simple
User=yourusername
WorkingDirectory=/path/to/linkedin-job-scraper
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/python run_agent.py
Restart=always
RestartSec=60

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable job-scraper
sudo systemctl start job-scraper
sudo systemctl status job-scraper
```

### Option 3: Windows Task Scheduler

1. Open Task Scheduler
2. Create Basic Task
3. Set trigger (e.g., At startup)
4. Action: Start a program
5. Program: `C:\path\to\venv\Scripts\python.exe`
6. Arguments: `C:\path\to\run_agent.py`
7. Start in: `C:\path\to\linkedin-job-scraper`

### Option 4: Docker (Advanced)

Create `Dockerfile`:
```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

# Install Chrome
RUN apt-get update && apt-get install -y wget gnupg
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list
RUN apt-get update && apt-get install -y google-chrome-stable

COPY . .

CMD ["python", "run_agent.py"]
```

Build and run:
```bash
docker build -t job-scraper .
docker run -d --name job-scraper --env-file .env job-scraper
```

## Cloud Deployment

### Heroku
1. Create `Procfile`: `worker: python run_agent.py`
2. Add buildpack for Chrome
3. Set config vars from `.env`
4. Deploy

### AWS EC2
1. Launch Ubuntu instance
2. Install Python and Chrome
3. Clone repository
4. Set up as systemd service
5. Configure security groups

### DigitalOcean
Similar to AWS EC2 setup

## Monitoring

### View Logs

**Systemd:**
```bash
sudo journalctl -u job-scraper -f
```

**Docker:**
```bash
docker logs -f job-scraper
```

### Check Job Data
```bash
python view_jobs.py
```

## Scaling

- Run multiple instances with different keywords
- Use separate databases per instance
- Implement rate limiting to avoid LinkedIn blocks

## Security

- Never expose `.env` file
- Use read-only filesystem where possible
- Regularly rotate LinkedIn password
- Monitor for unusual activity
