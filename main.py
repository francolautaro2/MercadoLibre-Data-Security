from google_drive import save_data
from send_email import send_email, mesagge
from database import connect_database, create_table, read_data
from classification import classification_response

from read_email import check_for_owner_response


def main():
    # Crea la tabla en la base de datos si esta no existe
    create_table()
    # Conexion a la base de datos para manejar consultas
    conn = connect_database()
    print("Running program...")
    
    while True:
        # Agrega nuevos archivos
        save_data()
        data = read_data(conn)
        for archivo in data:
            if archivo[5] == None:
                print("Correo enviado a:", archivo[3])
                msg = mesagge(archivo[3], archivo[1])
                send_email(msg, archivo[3])
                # Espera a que el usuario responda
                while True:
                    if check_for_owner_response(archivo[3]):
                        print("El usuario respondio")
                        classification_response(archivo[1], conn)
                        break
            
                print()
    
    conn.close()
main()
