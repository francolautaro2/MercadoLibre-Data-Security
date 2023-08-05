from database import create_table, insert_data, check_file_exists, connect_database, update_file
from google_drive import create_service, get_files
import os

def main():
    # Conexion a la base de datos
    conn = connect_database()
    cursor = conn.cursor()
    # Creamos la tabla en la base de datos
    create_table()

    # Conexion a la api de google drive
    service = create_service()
    # Obtenemos los archivos
    files = get_files(service)

    # Agrega los archivos en la base de datos
    for file in files:
        # Obtengo el nombre
        file_name = file["name"]
        # Obtengo la extension
        file_extension = os.path.splitext(file_name)[1]
        if file_extension == "":
            file_extension = "Folder"
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
        
    conn.close()
main()
