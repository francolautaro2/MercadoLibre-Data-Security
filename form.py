from database import connect_database, read_data
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from dotenv import load_dotenv
import os

# Cargamos las variables de entorno
load_dotenv()

email_sender = os.getenv("EMAIL_SENDER")
password_email = os.getenv("PASSWORD_EMAIL")

# Obtiene el nombre y la visibilidad del archivo 
def get_data():
    conn = connect_database()
    archivos = read_data(conn)
    values = []
    for i in archivos:
        values.append([i[1]])

    return values

def main():
    connection = connect_database()
    data = read_data(connection)

    archivos = []
    for fields in data:
        # Agrega el nombre de los archivos al array archivos
        archivos.append([fields[1], fields[3]])
    
    status, email_ids = mail.search(None, "(UNSEEN)")

    for archivo in archivos:
        name = archivo[0]
        owner = archivo[1]

        questions = [
        "¿Cuál es la importancia de este archivo?",
        "¿Quiénes tienen acceso a este archivo?",
        "¿Contiene información sensible?",
        ]
        
        questionnaire = "\n".join([f"{i+1}. {question}" for i, question in enumerate(questions)])
        email_subject = "Cuestionario de Clasificación de Archivo"
        email_body = f"Estimado/a {owner},\n\nPor favor, complete el siguiente cuestionario para ayudarnos a clasificar el archivo '{name}':\n\n{questionnaire}"

        msg = MIMEMultipart()
        msg['From'] = email_sender
        msg['To'] = owner
        msg['Subject'] = email_subject
        msg.attach(MIMEText(email_body, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email_sender, password_email)
        server.sendmail(email_sender, owner, msg.as_string())
        server.quit()

        # Esperar respuesta del usuario y clasificar el archivo
        # Procesar respuesta del usuario
        for email_id in email_ids[0].split():
            status, 
        classification = input(f"Clasificación del archivo '{name}' (Crítico/Alto/Medio/Bajo): ")


    connection.close()


if __name__ == '__main__':
    main()