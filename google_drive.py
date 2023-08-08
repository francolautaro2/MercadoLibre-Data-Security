from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from database import insert_data, check_file_exists, connect_database, update_visibility, read_data
import os

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive']

# Crea el servicio de google drive API
def create_drive_service():
    
    creds = None

    if os.path.exists('./credentials/drive_token.json'):
        creds = Credentials.from_authorized_user_file('./credentials/drive_token.json', SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                './credentials/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('./credentials/drive_token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('drive', 'v3', credentials=creds)

    return service

# Obtiene todos los archivos
def get_files(service_drive):
    results = service_drive.files().list(
    pageSize=1000, fields="files(id, name, owners, shared, mimeType)").execute()
    files = results.get('files', [])

    return files

# Para clasificar las carpetas (las carpetas no tienen extension en google drive)
# Clasifica el formulario
extensiones_types = {
    "folder": "application/vnd.google-apps.folder",
    "form": "application/vnd.google-apps.form"
}

# Guarda los datos del drive en una base de datos
def save_data(service_drive):
    # Conexion a la base de datos
    conn = connect_database()
    
    # Obtenemos los archivos
    files = get_files(service_drive)

    # Agrega los archivos en la base de datos
    for file in files:
        # Obtengo el id del file en drive
        file_id = file["id"]
        # Obtengo el nombre
        file_name = file["name"]
        # Obtengo la extension
        file_extension = os.path.splitext(file_name)[1]
        
        # Si la extension esta vacia significa que el archivo puede ser una carpeta o el formulario
        # Si es otro archivo no se detectara porque google drive no agrega extensiones a archivos creados dentro de google drive
        if file_extension == "":
            # Clasifica si es carpeta o formulario
            for key in extensiones_types:
                if file["mimeType"] == extensiones_types[key]:
                    file_extension = key

        # Obtengo el dueño
        owner = file["owners"][0]["emailAddress"] if "owners" in file else "Desconocido"
        # Obtengo la visibilidad
        if file["shared"] == True:
            visibility = "Publico"
        elif file["shared"] == False:
            visibility = "Privado"

        # Verifica si el archivo existe
        file_exist = check_file_exists(file_name, conn)
        # Si no existe lo agrega a la base de datos
        if file_exist == False:
            insert_data(file_id, file_name, file_extension, owner, visibility, conn)
        # Actualiza la visibilidad del archivo si este cambia
        update_visibility(visibility, file_name, conn)

    conn.close()

# Cambia el acceso de publico a privado
def change_public_access(id_file, service):
    # Elimina el acceso 
    delete_public_permissions = service.permissions().delete(fileId=id_file, permissionId="anyoneWithLink")
    delete_public_permissions.execute()
