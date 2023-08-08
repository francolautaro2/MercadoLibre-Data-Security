from google_drive import save_data, create_drive_service
from send_email import send_email, mesagge
from database import connect_database, create_table, read_data
from classification import classification_response

from read_email import check_for_owner_response


def main():
    # Crea la tabla en la base de datos si esta no existe
    create_table()
    # Conexion a la base de datos para manejar consultas
    
    print("Running program...")
    service = create_drive_service()
    
    while True:
        # Agrega nuevos archivos
        conn = connect_database()
        save_data(service)
        data = read_data(conn)
        for archivo in data:
            if archivo[6] == None:
                print()
                print("Correo enviado a:", archivo[4])
                msg = mesagge(archivo[4], archivo[2])
                send_email(msg, archivo[4])
                # Espera a que el usuario responda
                while True:
                    if check_for_owner_response(archivo[4]):
                        print("El usuario respondio")
                        classification_response(archivo[2], archivo[5], conn, service)
                        break
            
        conn.close()
    
main()
