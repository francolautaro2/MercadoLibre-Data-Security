from google_drive import save_data
from send_email import send_email, mesagge
from database import connect_database, read_data, create_table


def main():
    create_table()
    conn = connect_database()
    print("Running script...")
    while True:
        save_data()
        archivos = read_data(conn)
        for archivo in archivos:
            if archivo[5] == None:
                msg = mesagge(archivo[3], archivo[1])
                send_email(msg, archivo[3])
            
    conn.close()
main()
