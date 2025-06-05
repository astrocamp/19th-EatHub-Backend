import resend
import os
from dotenv import load_dotenv


load_dotenv()
resend.api_key = os.getenv('RESEND_API_KEY')
FROM_EMAIL = os.getenv('FROM_EMAIL')

def send_email(to_email, subject, html):
    resend.Emails.send({
        "from": FROM_EMAIL,
        "to": [to_email],
        "subject": subject,
        "html": html
    })