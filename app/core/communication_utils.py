import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from app.core.mongo_logging import log_to_mongo 

class EmailSendingException(Exception):
    pass

async def send_multi_email(recipients, subject, body):
    sender_email = os.getenv("NUTRIBOT_EMAIL_ACCOUNT")
    sender_password = os.getenv("NUTRIBOT_EMAIL_PASSWORD")
    smtp_server = "ssl0.ovh.net"
    smtp_port = 587
    
    email_sending_failure_count = 0

    for recipient in recipients:
        await log_to_mongo("EMAIL_SERVICE", "app/core/communication_utils/send_multi_email", "INFO", f"Sending email to {recipient}")
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
            await log_to_mongo("EMAIL_SERVICE", "app/core/communication_utils/send_multi_email", "INFO", f"Email SENT CORRECTLY to {recipient}")
        except Exception as e:
            await log_to_mongo("EMAIL_SERVICE", "app/core/communication_utils/send_multi_email", "ERROR", f"Failed to send email: {str(e)}")
            email_sending_failure_count += 1
    
    if email_sending_failure_count > 0:
        return 'Failed to send emails'
    else:
        return 'Emails sent successfully'
        
if __name__ == "__main__":
    import asyncio
    
    body = (
        f"Ciao alessio,<br><br>"
        "Il tuo nutrizionista ha richiesto una misurazione per te.<br>"
        "Per favore, clicca sul seguente link per iniziare il processo di misurazione:<br>"
        f"<a href='{'https://hypaz.com'}'>{'https://hypaz.com'}</a><br><br>"
        "Grazie,<br>"
        "Il team di NutriBot"
    )
    asyncio.run(
        send_multi_email(
            ['nutribot@hypaz.com'],
            "Richiesta di misurazione",
            body
        )
    )