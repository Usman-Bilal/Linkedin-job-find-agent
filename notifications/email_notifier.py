import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

class EmailNotifier:
    def __init__(self):
        self.enabled = os.getenv('ENABLE_EMAIL', 'false').lower() == 'true'
        self.to_email = os.getenv('EMAIL_TO')
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', 587))
        self.smtp_user = os.getenv('SMTP_USER')
        self.smtp_password = os.getenv('SMTP_PASSWORD')
    
    def send_job_notification(self, jobs):
        if not self.enabled or not jobs:
            return
        
        if not self.smtp_user or not self.smtp_password:
            print("Email credentials not configured")
            return
        
        try:
            msg = MIMEMultipart()
            msg['From'] = self.smtp_user
            msg['To'] = self.to_email
            msg['Subject'] = f'New Procurement Jobs Found - {len(jobs)} opportunities'
            
            body = self._create_email_body(jobs)
            msg.attach(MIMEText(body, 'html'))
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)
            
            print(f"Email notification sent to {self.to_email}")
        except Exception as e:
            print(f"Failed to send email: {e}")
    
    def _create_email_body(self, jobs):
        html = '<html><body><h2>New Procurement Jobs</h2><ul>'
        for job in jobs:
            html += f'''
            <li>
                <strong>{job["title"]}</strong><br>
                Company: {job["company"]}<br>
                Location: {job.get("location", "N/A")}<br>
                Source: {job["source"]}<br>
                <a href="{job["url"]}">View Job</a>
            </li><br>
            '''
        html += '</ul></body></html>'
        return html
