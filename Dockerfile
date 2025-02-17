FROM python:3.10-slim

# Evitamos que Python genere archivos .pyc y habilitamos el buffer de salida sin procesar
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Establecemos el directorio de trabajo dentro del contenedor
WORKDIR /IDEL_web_project

# Actualizamos el sistema e instalamos dependencias necesarias
RUN apt-get update && \
    apt-get install -y gcc libpq-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copiamos el archivo de requerimientos al directorio de trabajo actual
COPY requirements.txt .

# Actualizamos pip e instalamos las dependencias de Python
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copiamos el resto del código de la aplicación al contenedor
COPY . .

# Exponemos el puerto en el que correrá la aplicación (por defecto Django usa el 8000)
EXPOSE 8000

# Comando por defecto para levantar el servidor de desarrollo de Django
CMD ["python", "IDEL_web_project/manage.py", "runserver", "0.0.0.0:8000"]
