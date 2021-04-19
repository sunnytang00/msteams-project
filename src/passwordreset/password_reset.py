"""Bulk email many recipients
This class will send one email to a large group at once.
"""

import smtplib
from email.message import EmailMessage
from src.passwordreset.config_parser import ConfigParser
import json
import string
import random

class SendEmail:
    sender_email_address = ConfigParser.get('EMAIL', 'email_address')
    sender_email_password = ConfigParser.get('EMAIL', 'email_password')

    @classmethod
    def send_email(cls, subject, body, recipient):
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(cls.sender_email_address, cls.sender_email_password)
            msg = EmailMessage()
            msg['Subject'] = subject
            msg['From'] = cls.sender_email_address
            msg.set_content(body)

            smtp.send_message(msg=msg, to_addrs=recipient)
    
    @staticmethod
    def generate_reset_code(length=8):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
