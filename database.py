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

# Verifica si el archivo existe en la base de datos, si existe retorna True si no existe retorna False
def check_file_exists(name, conn):
    try:
        check_query = "SELECT * FROM drive_inventory WHERE name = %s"
        cursor = conn.cursor()
        cursor.execute(check_query, (name,))
        
        row = cursor.fetchone()
        if row is not None:
            return True  # Existe el archivo en la base de datos
        else:
            return False  # No existe el archivo en la base de datos
    
    except Error as e:
        print("Error al verificar archivos: ", e)
        return False

# Actualiza la visibilidad del archivo 
def update_visibility(visibility, file_name, conn):
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
def read_data(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM drive_inventory")
        result = cursor.fetchall()
    
    except Error as e:
        print("Error al consultar archivos: ", e)

    return result

# Actualiza la visibilidad del archivo
def update_criticality(new_criticality, file_name, conn):
    try:
        cursor = conn.cursor()
        # Sentencia SQL para actualizar la columna criticality
        update_query = f"UPDATE drive_inventory SET criticality = %s WHERE name = %s"
        update_values = (new_criticality.upper(), file_name)

        # Ejecuta la consulta de actualización
        cursor.execute(update_query, update_values)

        # Realiza la confirmación de la transacción
        conn.commit()
    except Error as e:
        print("Error al actualizar la criticidad del archivo: ", e)