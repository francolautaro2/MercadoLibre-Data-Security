import imaplib
import email
from email.header import decode_header
import os
from dotenv import load_dotenv

# Carga las variables de entorno
load_dotenv()

USERNAME = os.getenv("EMAIL_SENDER")
PASSWORD = os.getenv("PASSWORD_EMAIL")

# Conecta al servidor de imap
def server_connect():
    # Cargamos los datos
    imap_server = 'imap.gmail.com'
    mail = imaplib.IMAP4_SSL(imap_server)
    return mail


def read_email():
    # Se conecta al servidor y carga el username y password
    mail = server_connect()
    mail.login(USERNAME, PASSWORD)

    # Selecciona la bandeja de entrada 
    mailbox = 'INBOX'
    mail.select(mailbox)

    status, emails_ids = mail.search(None, 'UNSEEN')
    email_id_list = emails_ids[0].split()

    for email_id in email_id_list:
        status, msg_data = mail.fetch(email_id, '(RFC822)')
        raw_email = msg_data[0][1]
        email_message = email.message_from_bytes(raw_email)

        subject, encoding = decode_header(email_message['Subject'])[0]
        if isinstance(subject, bytes):
            subject = subject.decode(encoding or 'utf-8')
        if email_message.is_multipart():
            for part in email_message.walk():
                if part.get_content_type() == 'text/plain':
                    body = part.get_payload(decode=True).decode()
                    print("Asunto:", subject)
                    print("Cuerpo:", body)
                    print("-------------------")

        #Marcar el correo como leído
        mail.store(email_id, '+FLAGS', '\Seen')
    
    mail.logout()

while True:
    read_email()