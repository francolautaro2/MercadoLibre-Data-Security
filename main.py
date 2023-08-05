from database import create_table, insert_data, check_file_exists, connect_database, update_file, read_data
from google_drive import create_drive_service, get_files
import os

# Para clasificar las carpetas (las carpetas no tienen extension en google drive)
# Clasifica el formulario
extensiones_types = {
    "folder": "application/vnd.google-apps.folder",
    "form": "application/vnd.google-apps.form"
}

def main():
    # Conexion a la base de datos
    conn = connect_database()
    
    # Creamos la tabla en la base de datos
    create_table()

    # Conexion a la api de google drive
    service = create_drive_service()
    
    # Obtenemos los archivos
    files = get_files(service)

    # Agrega los archivos en la base de datos
    for file in files:
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
            insert_data(file_name, file_extension, owner, visibility, conn)
        # Actualiza la visibilidad del archivo si este cambia
        update_file(visibility, file_name, conn)

    conn.close()
main()
