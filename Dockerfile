# Usa una imagen base adecuada
FROM python:3.11

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos necesarios al contenedor
COPY . /app
# Actualiza pip
RUN pip install --upgrade pip
# Instalar dependencias de la app
RUN pip install -r requirements.txt

# Instala mysql
RUN apt-get update && apt-get install -y default-mysql-client

# Corro la aplicacion
CMD ["python", "main.py"]