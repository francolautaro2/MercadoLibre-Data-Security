# Caso - Documentación Pública
## Contexto
Se pidio realizar un script para que obtenga datos de archivos de google Drive, para luego enviar emails a los dueños de los archivos para que respondan un cuestionario con preguntas sobre las caracteristicas de los archivos con el fin de poder clasificarlos en un rango de (CRITICO, ALTO, MEDIO, BAJO). Los archivos que contengan la clasificacion de CRITICO o ALTO y esten publicos deberan ser cambiados a privados a la brevedad.

## Estrategias utilizadas
La estrategia que utilice para realizar el desafio fue usar la API de Google Drive para obtener la informacion de los archivos, almacenarlos en una base de datos MySQL para su posterior uso en los diferentes casos de clasificacion. Los archivos seran clasificados segun los criterios planteados en el archivo criterio.txt
El proyecto esta hecho en 6 scripts:
- `google_drive.py`: Este archivo maneja la conexion a la api de google drive y extrae la informacion necesaria de los archivos.
- `database.py`: Este archivo se ocupa de manejar todas las funciones relacionadas a la base de datos, leer, actualizar y extraer.
- `classification.py`: Contiene la funcion para clasificar el archivo por el usuario.
- `read_email.py`: Contiene la funcion encargada de leer los emails entrantes.
- `send_email.py`: Funcion para enviar emails dado un owner y archivo.
- `main.py`: Desde aqui se ejecutan todas las funciones.

## Requeriments
Para completar el correcto funcionamiento del programa siga los siguientes pasos:
1. Configure un proyecto en Google Cloud y habilite la API de Google Drive, una vez hecho eso descargue las credenciales.
Al archivo de credenciales que descargue por favor cambiar nombre a credentials.json y guardarlo en la carpeta credentials del proyecto.
https://cloud.google.com/endpoints/docs/frameworks/enable-api?hl=es-419
2. En el repositorio encontrara un archivo .env el cual contiene las variables de entorno necesarias para el funcionamiento correcto de la aplicacion
3. Una cuenta de gmail para enviar correos electronicos.
https://support.google.com/accounts/answer/185833?hl=es
4. Cree una base de datos en mysql para usar en el .env file.
5. Ejecute el siguiente comando: `pip install requirements.txt`.

## Descripcion del proceso de desarrollo
Nunca habia usado la API de Google Drive aunque fue muy lindo aprender a utilizarla, tiene muchas cosas que se pueden hacer con la misma. Otro problema que tuve fue que quise tambien usar la API de Google Forms para automatizar mejor el envio de cuestionarios a los owners de los diferentes archivos pero la misma se encuentra en version 1 y le faltan cosas para su correcto funcionamiento.

## Update 2.0.0 despues del feedback
### En la anterior version la key unica era el name, ahora se cambio a id para evitar errores con archivos que contengan el mismo nombre.
### Ahora la aplicacion se maneja con formularios de google y espera respuestas, no hace falta que se responda un cuestionario para seguir con el siguiente.
### Ahora la aplicacion pondera las respuestas de los usuarios mediante puntajes.
### Se ignoran los archivos que esten privados, solo se envian archivos publicos para ser clasificados.
### Se agrego el docker-compose.yml.
## Instrucciones
1. Configure en el google drive de la empresa una carpeta llamada formularios, ahi se van a almacenar todos los formularios de google para el cual van a ser enviados a los usuarios.
2. Cree un formulario de google que contenga preguntas cerradas de seguridad, yo use de ejemplo: ¿Este archivo contiene información confidencial o privada?, ¿La pérdida o daño de este archivo afectaría directamente la operación diaria?, ¿El archivo está relacionado con la cumplimiento de regulaciones legales o normativas?, ¿La información en este archivo es esencial para proyectos o tareas en curso?, ¿La falta de acceso a este archivo causaría retrasos significativos?, ¿Este archivo es necesario para la continuidad a largo plazo del negocio o proyecto? (Puede crear cuantas preguntas quiera, las preguntas deben tener de opcion solamente Si o No) 
3. En el archivo .env encontrara una variable llamada ID_FORMULARIO, alli debera pegar el id del formulario creado anteriormente.
4. Ejecute el programa `python main.py`
