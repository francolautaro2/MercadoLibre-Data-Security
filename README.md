# Caso - Documentación Pública
## Contexto
Se pidio realizar un script para que obtenga datos de archivos de google Drive, para luego enviar emails a los dueños de los archivos para que respondan un cuestionario con preguntas sobre las caracteristicas de los archivos con el fin de poder clasificarlos en un rango de (CRITICO, ALTO, MEDIO, BAJO). Los archivos que contengan la clasificacion de CRITICO o ALTO y esten publicos deberan ser cambiados a privados a la brevedad.

## Estrategias utilizadas
La estrategia que utilice para realizar el desafio fue usar la API de Google Drive para obtener la informacion de los archivos, almacenarlos en una base de datos MySQL para su posterior uso en los diferentes casos de clasificacion.
El proyecto esta hecho en 6 scripts:
- google_drive.py: Este archivo maneja la conexion a la api de google drive y extrae la informacion necesaria de los archivos.
- database.py: Este archivo se ocupa de manejar todas las funciones relacionadas a la base de datos, leer, actualizar y extraer.
- classification.py: Contiene la funcion para clasificar el archivo por el usuario.
- read_email.py: Contiene la funcion encargada de leer los emails entrantes.
- send_email.py: Funcion para enviar emails dado un owner y archivo.
- main.py: Desde aqui se ejecutan todas las funciones.
