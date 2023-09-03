from __future__ import print_function

import os.path
from database import update_visibility
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os
from database import update_visibility, update_criticality
# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive']


# Obtiene los archivos de google drive 
async def get_drive():
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

    service_drive = build('drive', 'v3', credentials=creds)
    return service_drive


# Crea una lista con todos los datos de los archivos
async def get_files(service_drive):
    
    results = service_drive.files().list(
        q="mimeType != 'application/vnd.google-apps.folder' and not name contains 'Formulario' and not name contains 'seguridad'", pageSize=1000, fields="files(id, name, owners, shared, mimeType)").execute()
    result = results.get('files', [])
    data = []
    
    for i in result:
        id = i["id"]
        name = i["name"]
        owner_email = i["owners"][0]["emailAddress"]
        if i["shared"] == True:
            visibility = "Publico"
        elif i["shared"] == False:
            visibility = "Privado"
            # Si el archivo es privado lo clasifica como critico
            await update_criticality("CRITICO", id)
        file_extension = os.path.splitext(name)[1]
        if file_extension == "":
            ext = i["mimeType"]
            parts = ext.split('.')
            file_extension = parts[-1]

        await update_visibility(visibility,id)
        
        data.append([id, name,file_extension, owner_email, visibility])
    
    return data

# Cambia el acceso de publico a privado
async def change_public_access(service, id_file):
    # Elimina el acceso 
    delete_public_permissions = service.permissions().delete(fileId=id_file, permissionId="anyoneWithLink")
    delete_public_permissions.execute()