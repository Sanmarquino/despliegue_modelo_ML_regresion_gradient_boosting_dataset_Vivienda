# 1. Imagen base oficial de Linux Debian con Python 3.14 ligero (igual a tu entorno .venv)
FROM python:3.14-slim

# 2. Variables de entorno para optimizar Python dentro de contenedores
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Carpeta de trabajo interna dentro del contenedor Linux
WORKDIR /app

# 4. Copiamos primero requirements.txt e instalamos librerías (aprovecha la caché de capas de Docker)
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 5. Copiamos únicamente los archivos necesarios para servir la API en producción
COPY esquemas.py main.py modelo_bundle_viviendas.joblib ./

# 6. Documentamos que el contenedor escucha en el puerto 8000
EXPOSE 8000

# 7. Comando de arranque con --host 0.0.0.0 para aceptar tráfico desde fuera del contenedor
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]