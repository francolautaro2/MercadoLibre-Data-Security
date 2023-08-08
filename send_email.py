from database import read_data, connect_database
import os
from dotenv import load_dotenv
import smtplib
import imaplib
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Carga las variables de entorno de email
load_dotenv()

# Configuracion de las cuentas de gmail y los servidores de email
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
IMAP_SERVER = 'imap.gmail.com'
IMAP_PORT = 993
EMAIL_SENDER =  os.getenv("EMAIL_SENDER")
PASSWORD = os.getenv("PASSWORD_EMAIL")

# Preguntas para realizar al dueño del archivo
PREGUNTAS = [
    "¿Este archivo es esencial para el funcionamiento de la organización?",
    "¿La pérdida o inaccesibilidad de este archivo tendría un impacto catastrófico?",
    "¿Este archivo contiene información confidencial o personal?",
    "¿Este archivo está relacionado con la operación crítica de algún proceso?",
    "¿Es necesario mantener este archivo para cumplir con regulaciones o normativas?",
]

# Obtiene los valores de name_file y owner
def get_values():
    conn = connect_database()
    values = read_data(conn)
    # obtengo el nombre del archivo y el propietario
    archivos = []
    for value in values:
        if value[5] == None:
            archivos.append([value[1], value[3]])
        else:
            print("Los archivos ya han sido clasificados")
    
    return archivos

# Crea el Mensaje para cada dueño con su archivo correspondiente
def mesagge(owner, file_name):
    asunto = "Cuestionario de Clasificacion de Archivo"
    cuestionario = "\n".join([f"{i + 1}. {pregunta}" for i, pregunta in enumerate(PREGUNTAS)])
    cuerpo_email = f"Estimado/a {owner},\n\nPor favor, complete el siguiente cuestionario para ayudarnos a clasificar el archivo '{file_name}':\n\n{cuestionario}"
    message = MIMEMultipart()
    message['From'] = EMAIL_SENDER
    message['To'] = owner
    message['Subject'] = asunto
    message.attach(MIMEText(cuerpo_email, 'plain'))
    
    return message

# Envia al email el nombre del archivo y las preguntas
def send_email(msg, owner):
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(EMAIL_SENDER, PASSWORD)
    server.sendmail(EMAIL_SENDER,owner, msg.as_string())
    server.quit()