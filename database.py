import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv


# Carga las variables de entorno
load_dotenv()

# Funcion para conectarse a la base de datos del inventario
def connect_database():
    conn = mysql.connector.connect(
        user=os.getenv("USER"),
        password=os.getenv("PASSWORD"),
        host=os.getenv("HOST"),
        database=os.getenv("DATABASE")
    )
    return conn

# Creamos la tabla en la base de datos
def create_table():
    try:
        conn = connect_database()
        cursor = conn.cursor()

        with open("./database/inventory.sql", "r") as sql_file:
            sql_script = sql_file.read()

        sql_commands = sql_script.split(';')

        for command in sql_commands:
            if command.strip():
                cursor.execute(command)

        conn.commit()
        
    except Error as e:
        print("Error en la base de datos: ", e)


# Funcion para insertar los datos en la tabla inventory_drive
def insert_data(name, extension, owner, visibilidad, conn):
    try:
        cursor = conn.cursor()

        sql_insert_query = "INSERT INTO drive_inventory (name, extension, owner, visibility) VALUES (%s, %s, %s, %s)"
        data = (name, extension, owner, visibilidad)

        cursor.execute(sql_insert_query, data)

        conn.commit()
    
    except Error as e:
        print("Error al insertar datos: ", e)
    finally:
        if conn:
            conn.close()

# Verifica si el archivo existe en la base de datos, si existe retorna 1 si no existe retorna 0
def chek_file_exists(name, conn):
    try:
        check_query = "SELECT COUNT(*) FROM drive_inventory WHERE name = %s"
        cursor = conn.cursor()
        cursor.execute(check_query, (name,))
        
        file_count = cursor.fetchone()[0]
    
    except Error as e:
        print("Error al verificar archivos: ", e)
        
    return file_count

# Actualiza la visibilidad del archivo 
def update_file(visibility, file_name, conn):
    try:
        cursor = conn.cursor()
        # Actualizo la visibilidad del archivo
        update_query = "UPDATE drive_inventory SET visibility = %s WHERE name = %s"
        update_data = (visibility, file_name)
        cursor.execute(update_query,update_data)
        conn.commit()
    
    except Error as e:
        print("Error al actualizar archivo: ", e)

# Funcion para leer los datos de la base de datos
def read_data():
    pass