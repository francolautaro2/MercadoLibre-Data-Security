from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

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
    pageSize=1000, fields="files(name, owners, shared, mimeType)").execute()
    files = results.get('files', [])

    return files
