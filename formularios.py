'''
Crear un formulario por cada archivo en la base de datos
    - la idea es leer la base de datos y apartir del name del archivo crear el form
        - obtener datos de la base de datos
        - verificar si el archivo es privado o publico
        - verificar si el archivo ya ha sido clasificado
'''
from __future__ import print_function

# importo google drive para una prueba
from google_drive import get_drive

import asyncio

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os

from ponderation import asignar_clasificacion_ponderada

from dotenv import load_dotenv

load_dotenv()


SCOPES = ['https://www.googleapis.com/auth/forms.body', "https://www.googleapis.com/auth/forms.responses.readonly"]
SCOPES_DRIVE = ['https://www.googleapis.com/auth/drive']
DISCOVERY_DOC = "https://forms.googleapis.com/$discovery/rest?version=v1"

# Se conecta a la api de google forms
async def get_forms_service():
    creds = None
    if os.path.exists('./credentials/forms_token.json'):
        creds = Credentials.from_authorized_user_file('./credentials/forms_token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                './credentials/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('./credentials/forms_token.json', 'w') as token:
            token.write(creds.to_json())


    service = build('forms', 'v1', credentials=creds)

    return service


# Crea un formulario nuevo
async def create_forms(form_service, drive_service, files):
    formularios_creados = {}
    origin_file_id = os.getenv("ID_FORM")
    
    for id, name, owner in files:
        
        results = drive_service.files().copy(
        fileId=origin_file_id).execute()

        update = {
            "requests": [{
                "updateFormInfo": {
                    "info": {
                        "title": f"Formulario de seguridad del archivo: {name}",
                    },
                    "updateMask": "title"
                }
            }]
        }
        
        # Actualiza el nombre del archivo
        drive_service.files().update(fileId=results["id"], body={'name':"Formulario de seguridad del archivo: "+name}).execute()
        # Actualiza el titulo del archivo
        form_service.forms().batchUpdate(formId=results["id"], body=update).execute()
        formularios_creados[results["id"]] = [id,name,owner]
        
    return formularios_creados

# Lee las respuestas de los formularios creados
async def read_responses(service_form, service_drive, formularios):
    while formularios != {}:
        print("Esperando Respuestas...")
        for form_id, form_info in list(formularios.items()):
            
            result = service_form.forms().responses().list(formId=form_id).execute()
            # Para detectar si el usuario respondio
            if result != {}:
                respuestas = []
                for response in result['responses']:
                    for answer in response['answers'].values():
                        value = answer['textAnswers']['answers'][0]['value']
                        respuestas.append(value)
                form_name = form_info[1]
                file_id = form_info[0]
                await asignar_clasificacion_ponderada(respuestas, file_id)
                print("Los valores para el formulario:", form_name, "son:", respuestas)
                print("Formulario eliminado")
                service_drive.files().delete(fileId=form_id).execute()
                
                del formularios[form_id]
        await asyncio.sleep(10)
        