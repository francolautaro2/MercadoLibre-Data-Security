import aiomysql
import os
from dotenv import load_dotenv

load_dotenv()

# Guarda los archivos en la base de datos
async def guardar_datos(data_list):
    # Conexion a la base de datos
    pool = await aiomysql.create_pool(
        host=os.getenv("HOST"),
        port=int(os.getenv("PORT")),
        user=os.getenv("USER"),
        password=os.getenv("DB_PASSWORD"),
        db=os.getenv("DATABASE"),
        autocommit=True
    )
    # Query para guardar datos
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            for data in data_list:
                fileId = data[0]
                await cur.execute(
                    "SELECT fileId, name, extension, owner, visibility FROM drive_inventory WHERE fileId = %s",
                    (fileId,)
                )
                existing_record = await cur.fetchone()
                if existing_record:
                    # Si existe un registro con el mismo id
                    print(f"ID: '{fileId}' ya existe en la base de datos.")
                else:
                    await cur.execute(
                        "INSERT INTO drive_inventory (fileId, name, extension, owner, visibility) VALUES (%s, %s, %s, %s, %s)",
                        (data[0], data[1], data[2], data[3], data[4])
                    )
                    print(f"ID: '{fileId}' insertado en la base de datos.")
            print("Datos guardados en la base de datos")

# Actualiza la criticidad de un archivo
async def update_criticality(new_criticality, file_id):
    pool = await aiomysql.create_pool(
        host=os.getenv("HOST"),
        port=int(os.getenv("PORT")),
        user=os.getenv("USER"),
        password=os.getenv("DB_PASSWORD"),
        db=os.getenv("DATABASE"),
        autocommit=True
    )

    try:
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                # Sentencia SQL para actualizar la columna criticality
                update_query = f"UPDATE drive_inventory SET criticality = %s WHERE fileId = %s"
                update_values = (new_criticality.upper(), file_id)

                # Ejecuta la consulta de actualización
                await cursor.execute(update_query, update_values)

                # No es necesario commit con autocommit=True
    except aiomysql.Error as e:
        print("Error al actualizar la criticidad del archivo: ", e)

# Actualiza la visibilidad del archivo
async def update_visibility(visibility, file_id):
    pool = await aiomysql.create_pool(
        host=os.getenv("HOST"),
        port=int(os.getenv("PORT")),
        user=os.getenv("USER"),
        password=os.getenv("DB_PASSWORD"),
        db=os.getenv("DATABASE"),
        autocommit=True
    )
    
    try:
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                # Actualizo la visibilidad del archivo
                update_query = "UPDATE drive_inventory SET visibility = %s WHERE fileId = %s"
                update_data = (visibility, file_id)
                await cursor.execute(update_query, update_data)
                await conn.commit()

    except aiomysql.Error as e:
        print("Error al actualizar archivo: ", e)


# Obtener datos no clasificados
async def obtener_datos_no_clasificados():
    pool = await aiomysql.create_pool(
        host=os.getenv("HOST"),
        port=int(os.getenv("PORT")),
        user=os.getenv("USER"),
        password=os.getenv("DB_PASSWORD"),
        db=os.getenv("DATABASE"),
    )
    
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("SELECT fileId, name, owner FROM drive_inventory WHERE criticality IS NULL AND visibility = 'PUBLICO'")
            files = await cur.fetchall()
    return files