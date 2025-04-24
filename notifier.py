
# notifier.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

class Notifier:
    def __init__(self, email_enabled=False, smtp_settings=None):
        self.email_enabled = email_enabled
        self.smtp_settings = smtp_settings or {}

    def notify(self, subject, message):
        print(f"📣 NOTIFICATION: {subject}\n{message}")
        if self.email_enabled:
            self._send_email(subject, message)

    def _send_email(self, subject, body):
        try:
            msg = MIMEMultipart()
            msg["From"] = self.smtp_settings.get("from")
            msg["To"] = self.smtp_settings.get("to")
            msg["Subject"] = subject
            msg.attach(MIMEText(body, "plain"))

            with smtplib.SMTP(self.smtp_settings.get("host"), self.smtp_settings.get("port")) as server:
                server.starttls()
                server.login(self.smtp_settings.get("user"), self.smtp_settings.get("pass"))
                server.send_message(msg)

            print("✅ Email sent.")
        except Exception as e:
            print(f"❌ Email failed: {e}")
