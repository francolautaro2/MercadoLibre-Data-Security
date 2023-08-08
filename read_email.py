import imaplib
import email
from dotenv import load_dotenv
import os


load_dotenv()

def check_for_owner_response(owner):
    IMAP_SERVER = 'imap.gmail.com'
    IMAP_PORT = 993
    EMAIL_ADDRESS = os.getenv("EMAIL_SENDER")
    EMAIL_PASSWORD = os.getenv("PASSWORD_EMAIL")

    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    mail.select('inbox')

    result, data = mail.search(None, f'FROM "{owner}" UNSEEN')
    if result == 'OK':
        for num in data[0].split():
            result, msg_data = mail.fetch(num, '(RFC822)')
            if result == 'OK':
                raw_email = msg_data[0][1]
                msg = email.message_from_bytes(raw_email)
                return True

    mail.logout()
    return False