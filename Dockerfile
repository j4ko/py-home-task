# Paso 1: Usar una imagen oficial de Python como imagen base.
# Se elige una versión 'slim' porque es más ligera que la completa.
FROM python:3.11-slim

# Paso 2: Establecer el directorio de trabajo dentro del contenedor.
# Todas las acciones posteriores (copiar, ejecutar) se harán relativas a esta ruta.
WORKDIR /app

# Paso 3: Instalar la dependencia de pytest.
# Para simplificar, en lugar de un fichero requirements.txt, la instalamos directamente.
RUN python3 -m pip install --no-cache-dir pytest

# Paso 4: Copiar los ficheros del proyecto al directorio de trabajo.
# Se copia el script de test y la carpeta de datos.
COPY test_data_validation.py .
COPY data/ ./data/

# Paso 5: Definir el comando que se ejecutará cuando el contenedor se inicie.
# Este es el comando que nos pediste para ejecutar los tests.
CMD ["python3", "-m", "pytest", "-v"]
