import os.path
import json
from database import connect_database, read_data


from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


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

preguntas = [
    {
        "questionItem": {
            "question": {
                "choiceQuestion": {
                    "options": [
                        {
                            "value": "CRITICO"
                        },
                        {
                            "value": "ALTO"
                        },
                        {
                            "value": "MEDIO"
                        },
                        {
                            "value": "BAJO"
                        }
                    ],
                    "type": "RADIO"
                },
            }
        },
        "title": "¿En qué medida este archivo es crucial para las operaciones o actividades del negocio?"
    },
    {
        "questionItem": {
            "question": {
                "choiceQuestion": {
                    "options": [
                        {
                            "value": "SI"
                        },
                        {
                            "value": "NO"
                        }
                    ],
                    "type": "RADIO"
                },
            }
        },
        "title": "¿El archivo contiene información confidencial, privada o sensible?"
    },
    {
        "questionItem": {
            "question": {
                "choiceQuestion": {
                    "options": [
                        {
                            "value": "CRITICO"
                        },
                        {
                            "value": "ALTO"
                        },
                        {
                            "value": "MEDIO"
                        },
                        {
                            "value": "BAJO"
                        }
                    ],
                    "type": "RADIO"
                },
            }
        },
        "title": "Si el archivo se pierde o se filtra, ¿cuál sería el impacto en términos de confidencialidad, integridad y disponibilidad de la información?"
    },
    {
        "questionItem": {
            "question": {
                "choiceQuestion": {
                    "options": [
                        {
                            "value": "ALTO"
                        },
                        {
                            "value": "MEDIO"
                        },
                        {
                            "value": "BAJO"
                        }
                    ],
                    "type": "RADIO"
                },
            }
        },
        "title": "¿Con qué frecuencia se necesita acceder a este archivo? ¿Es necesario acceder rápidamente en situaciones críticas?"
    },
    {
        "questionItem": {
            "question": {
                "choiceQuestion": {
                    "options": [
                        {
                            "value": "SI"
                        },
                        {
                            "value": "NO"
                        }
                    ],
                    "type": "RADIO"
                },
            }
        },
        "title": "¿El archivo está sujeto a regulaciones o requisitos de cumplimiento?"
    },
    {
        "questionItem": {
            "question": {
                "choiceQuestion": {
                    "options": [
                        {
                            "value": "SI"
                        },
                        {
                            "value": "NO"
                        }
                    ],
                    "type": "RADIO"
                },
            }
        },
        "title": "¿Otros procesos o sistemas dependen de este archivo para funcionar correctamente?"
    },
]

# Plantilla del JSON
form = {
    "formId": "1G0o0I6xZyu3Etn36UgKcwgwqTfz3ja6mGlIbYkbZres",
    "info": {
        "documentTitle": "Formulario sin título",
        "title": "Criticidad de Archivos"
    },
    "items": [
       
    ],
    "responderUri": "https://docs.google.com/forms/d/e/1FAIpQLSdrW5P6cPXl8WNJULEzE0_bCmld0pwWxOY65ijtDcNc45JTWw/viewform"
}


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
        else:
            continue

    return form

names = get_names_db()
form = create_form(names)

print(json.dumps(form, indent=4))
