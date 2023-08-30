import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

# Funcion para enviar correos
async def enviar_correo(destinatario, archivo, url_formulario, smtp_server, smtp_port, smtp_username, smtp_password):
    # Crear el objeto MIMEMultipart para el correo
    msg = MIMEMultipart()
    msg['From'] = "francolau03@gmail.com"
    msg['To'] = destinatario
    msg['Subject'] = archivo 
     
    # Agregar el contenido del correo
    mensaje = f"Estimado dueno,\n\nAdjunto encontrara su archivo importante: {archivo}.\n \nAbrir el link enviado en una pestaña en incognito, para evitar errores\nResponda el siguiente cuestionario para poder clasificarlo: {url_formulario} \n\nSaludos,\nTu Equipo"
    msg.attach(MIMEText(mensaje, 'plain'))

    # Iniciar la conexión al servidor SMTP y enviar el correo
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(msg['From'], msg['To'], msg.as_string())


archivos_enviados = []
async def enviar_correos(drive_service,formularios):
    
    # Configurar los detalles del servidor SMTP
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_username = os.getenv("EMAIL_SENDER")
    smtp_password = os.getenv("PASSWORD_EMAIL")

    for formId, data in formularios.items():
        # Obtiene la url para compartir el archivo
        url_formulario = drive_service.files().get(fileId=formId, fields='webViewLink').execute().get("webViewLink")

        if data[0] not in archivos_enviados:
            await enviar_correo(data[2], data[1], url_formulario, smtp_server, smtp_port, smtp_username, smtp_password)
            archivos_enviados.append([formId, data[1], data[2]])