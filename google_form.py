import os.path
import json
from database import connect_database, read_data


from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from questions_form import preguntas, form

SCOPES = ["https://www.googleapis.com/auth/forms.body"]

# Crea un servicio de api forms
def create_form_service():

    creds = None

    if os.path.exists('./credentials/form_token.json'):
        creds = Credentials.from_authorized_user_file('./credentials/form_token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                './credentials/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('./credentials/form_token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('forms', 'v1', credentials=creds)

    return service


# BatchUpdate para agregar o actualizar contenido del form

# Obtiene los nombres y la criticidad de los archivos en la base de datos
def get_names_db():
    conn = connect_database()
    results = read_data(conn)

    names =[]
    for file in results:
        names.append([file[1], file[5]])
    
    return names

# Crea el formulario con los archivos que hay en la base de datos
def create_form(file_names):
    # Iterar a través de los nombres de archivos y agregarlos al diccionario
    for nombre_archivo in names:
        # Si la criticidad del archivo en la base de datos es null, entonces lo agrega al formulario
        if nombre_archivo[1] == None:
            archivo = {
                "pageBreakItem": {},
                "title": nombre_archivo[0]
            }
            form["items"].append(archivo)
            form["items"].extend(preguntas)

    return form

names = get_names_db()
form = create_form(names)

print(json.dumps(form, indent=4))

def create_form_api():
    pass
