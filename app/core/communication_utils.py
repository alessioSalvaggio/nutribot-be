import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

class EmailSendingException(Exception):
    pass

def send_email(recipient, subject, body):
    sender_email = os.getenv("NUTRIBOT_EMAIL_ACCOUNT")
    sender_password = os.getenv("NUTRIBOT_EMAIL_PASSWORD")
    smtp_server = "ssl0.ovh.net"
    smtp_port = 587

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient
    message["Subject"] = subject
    message.attach(MIMEText(body, "html"))  

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient, message.as_string())
        server.quit()
        return {"message": "Email sent successfully"}
    except Exception as e:
        raise EmailSendingException(f"Failed to send email: {str(e)}")
