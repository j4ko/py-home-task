
# Solución de Validación de Datos con Pytest

## Descripción General

Esta solución utiliza Python y el framework de testing `pytest` para realizar una serie de validaciones sobre un fichero de datos (`data/rt-feed-record`) que contiene registros en formato JSON-line.

El objetivo es asegurar la integridad, completitud y formato correcto de los datos recibidos en tiempo real.

## Proceso de Validación

El script `test_data_validation.py` implementa tres tests independientes:

### 1. Conteo de Documentos Únicos (`test_count_unique_documents`)

- **Propósito**: Verificar el número total de documentos distintos en el fichero de datos.
- **Proceso**: El test lee el fichero línea por línea, extrae el campo `RP_DOCUMENT_ID` de cada registro JSON y lo añade a un `set` para garantizar la unicidad. Finalmente, verifica que el número total de IDs únicos sea mayor que cero y reporta la cantidad encontrada.

### 2. Verificación de Analíticas Incompletas (`test_find_documents_with_missing_analytics`)

- **Propósito**: Detectar si a algún documento le faltan partes (analíticas).
- **Proceso**: Agrupa todos los registros por su `RP_DOCUMENT_ID`. Para cada documento, compara el número de analíticas que se esperaban (según el campo `DOCUMENT_RECORD_COUNT`) con las que realmente se han encontrado (contando los `DOCUMENT_RECORD_INDEX` únicos). Si no coinciden, el test falla y reporta exactamente qué documentos están incompletos y qué índices de analíticas faltan.

### 3. Validación de Formato de ID de Entidad (`test_rp_entity_id_format`)

- **Propósito**: Asegurar que el campo `RP_ENTITY_ID` cumple con el formato esperado.
- **Proceso**: Basado en un análisis previo de los datos, se determinó que el formato correcto es una cadena alfanumérica de 6 caracteres en mayúsculas. Este test utiliza una expresión regular (`^[A-Z0-9]{6}$`) para validar cada `RP_ENTITY_ID` en el fichero. Si algún ID no cumple con este formato, el test falla y reporta el valor incorrecto y el número de línea donde fue encontrado.

## Cómo Ejecutar los Tests

Para ejecutar la suite de validación, sitúese en el directorio raíz del proyecto y ejecute el siguiente comando:

```bash
python3 -m pytest -v
```
