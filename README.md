# Caso - Documentación Pública
## Contexto
Se pidio realizar un script para que obtenga datos de archivos de google Drive, para luego enviar emails a los dueños de los archivos para que respondan un cuestionario con preguntas sobre las caracteristicas de los archivos con el fin de poder clasificarlos en un rango de (CRITICO, ALTO, MEDIO, BAJO). Los archivos que contengan la clasificacion de CRITICO o ALTO y esten publicos deberan ser cambiados a privados a la brevedad.

## Estrategias utilizadas
El proyecto se divide en 6 scripts de python.
S
- google_drive.py: Este archivo maneja la conexion a la api de google drive y extrae la informacion necesaria de los archivos.
- database.py: Este archivo se ocupa de manejar todas las funciones relacionadas a la base de datos, leer, actualizar y extraer.
- classification.py: Este archivo contiene la funcion para clasificar el archivo dado.
- read_email.py: Archivo para leer los emails entrantes y tener las respuestas de los diferentes emails enviados.
- send_email.py: Se ocupa de enviar los emails con la informacion necesaria. 
