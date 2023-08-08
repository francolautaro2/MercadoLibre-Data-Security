# Usa una imagen base de Python
FROM python:3.8

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos necesarios al contenedor
COPY requirements.txt .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto de los archivos al contenedor
COPY . .

# Comando por defecto para ejecutar cuando se inicie el contenedor
CMD ["python", "main.py"]