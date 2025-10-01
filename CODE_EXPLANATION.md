
# Análisis Detallado del Código: `test_data_validation.py`

Este documento explica línea por línea el script de testing `test_data_validation.py`.

---

### **Importaciones**

```python
import json
import pytest
import re
from pathlib import Path
```

- `import json`: Necesario para parsear (convertir) las líneas de texto en formato JSON a objetos de Python (diccionarios).
- `import pytest`: Importa el framework de testing. Lo usamos para funcionalidades avanzadas como `pytest.fail()`, que nos permite fallar un test con un mensaje personalizado.
- `import re`: Importa el módulo de expresiones regulares, utilizado para la validación de patrones de texto en el test de formato de `RP_ENTITY_ID`.
- `from pathlib import Path`: Proporciona una forma moderna y orientada a objetos para manejar rutas de ficheros, haciendo el código más legible y compatible entre diferentes sistemas operativos (Windows, macOS, Linux).

---

### **Función `test_count_unique_documents()`**

Este test cuenta el número total de documentos únicos en el fichero.

```python
# Define la ruta al fichero de datos de forma relativa al script actual.
# __file__ es una variable que contiene la ruta del fichero .py que se está ejecutando.
# .parent se refiere al directorio padre, y / "data" / "rt-feed-record" construye la ruta.
data_file_path = Path(__file__).parent / "data" / "rt-feed-record"

# Se inicializa un `set` vacío. Un set es una colección que no permite elementos duplicados,
# por lo que es la estructura de datos ideal para contar elementos únicos de forma eficiente.
unique_document_ids = set()
```

El test abre el fichero y lo lee línea por línea. Este método es eficiente en memoria, ya que no carga el fichero completo de una vez.

```python
try:
    with data_file_path.open('r', encoding='utf-8') as f:
        for line in f:
            # Si la línea está en blanco, la ignora y continúa con la siguiente.
            if not line.strip():
                continue
            try:
                # Intenta parsear la línea como un objeto JSON.
                data = json.loads(line)
                # Si el JSON tiene la clave 'RP_DOCUMENT_ID', añade su valor al set.
                # Si el ID ya está en el set, no ocurre nada.
                if 'RP_DOCUMENT_ID' in data:
                    unique_document_ids.add(data['RP_DOCUMENT_ID'])
            # Si una línea no es un JSON válido, imprime un aviso pero no detiene el test.
            except json.JSONDecodeError:
                print(f"Warning: Could not decode JSON line: {line.strip()}")
# Si el fichero de datos no se encuentra, el test falla inmediatamente con un mensaje claro.
except FileNotFoundError:
    pytest.fail(f"Data file not found at path: {data_file_path}", pytrace=False)
```

Finalmente, se reporta el resultado y se realiza la aserción.

```python
# Se calcula el número total de documentos únicos obteniendo el tamaño (len) del set.
total_unique_documents = len(unique_document_ids)

# Se imprime el resultado en la consola para verificación manual.
print(f"\nThe total number of unique documents found is: {total_unique_documents}")

# `assert` es la declaración principal de un test. Comprueba si una condición es verdadera.
# Aquí, se asegura de que el script al menos encontró un documento.
assert total_unique_documents > 0
```

---

### **Función `test_find_documents_with_missing_analytics()`**

Este test busca documentos a los que les falten analíticas.

```python
# Se inicializa un diccionario vacío. Se usará para agrupar todas las analíticas
# por su ID de documento.
# La estructura será: {'doc_id_1': {'expected_count': 10, 'indices': {1, 2, 5, ...}}, ...}
documents = {}
```

El núcleo del test itera sobre el fichero y construye la estructura de datos `documents`.

```python
# ... (apertura del fichero similar al test anterior) ...
for line in f:
    # ... (parseo del JSON similar al test anterior) ...
    doc_id = data.get('RP_DOCUMENT_ID')
    record_count = data.get('DOCUMENT_RECORD_COUNT')
    record_index = data.get('DOCUMENT_RECORD_INDEX')

    # Si al registro le falta alguno de los campos clave, se ignora.
    if not all([doc_id, record_count, record_index]):
        continue

    # Si es la primera vez que vemos este ID de documento...
    if doc_id not in documents:
        # ...se crea una nueva entrada en el diccionario.
        documents[doc_id] = {
            'expected_count': record_count, # Se guarda el número esperado de partes.
            'indices': {record_index}      # Se crea un nuevo set con el índice actual.
        }
    else:
        # Si el ID ya existía, simplemente se añade el nuevo índice al set existente.
        documents[doc_id]['indices'].add(record_index)
```

Una vez procesado todo el fichero, se pasa a la fase de verificación.

```python
# Se crea una lista para guardar los mensajes de error de los documentos incompletos.
incomplete_documents = []
# Se itera sobre cada documento que hemos agrupado.
for doc_id, data in documents.items():
    expected_count = data['expected_count']
    received_indices = data['indices']

    # Se crea un `set` "perfecto" con todos los índices que deberíamos haber recibido.
    # ej: si expected_count es 5, esto crea {1, 2, 3, 4, 5}.
    expected_indices = set(range(1, expected_count + 1))

    # Si el set de índices recibidos no es igual al set de índices esperados...
    if received_indices != expected_indices:
        # ...significa que hay un problema. Se calculan las diferencias.
        missing_indices = sorted(list(expected_indices - received_indices))
        extra_indices = sorted(list(received_indices - expected_indices))
        # Se construye un mensaje de error detallado.
        error_message = f"Document ID: {doc_id} -> ..."
        # Se añade el mensaje a la lista de documentos incompletos.
        incomplete_documents.append(error_message)

# Al final, si la lista de errores no está vacía...
if incomplete_documents:
    # ...se unen todos los mensajes de error en un solo reporte.
    report = "\n".join(incomplete_documents)
    # ...y el test falla, mostrando el reporte detallado en la consola.
    # `pytrace=False` hace que la salida de pytest sea más limpia, ocultando el traceback de Python.
    pytest.fail(f"...\n{report}", pytrace=False)
```

---

### **Función `test_rp_entity_id_format()`**

Este test valida que el formato del campo `RP_ENTITY_ID` sea correcto.

```python
# Se compila una expresión regular. Compilarla de antemano es más eficiente si se usa muchas veces.
# El patrón `^[A-Z0-9]{6}$` significa:
# ^      -> inicio de la cadena
# [A-Z0-9] -> cualquier carácter que sea una letra mayúscula o un dígito
# {6}    -> exactamente 6 veces
# $      -> fin de la cadena
id_pattern = re.compile(r"^[A-Z0-9]{6}$")

# Se inicializa una lista para guardar los errores de formato encontrados.
invalid_ids = []
```

El test itera sobre el fichero, validando cada ID.

```python
# ... (apertura del fichero similar a los tests anteriores) ...
# `enumerate(f, 1)` nos da tanto la línea como un contador (empezando en 1) para el número de línea.
for i, line in enumerate(f, 1):
    # ... (parseo del JSON) ...
    entity_id = data.get('RP_ENTITY_ID')

    # Si el campo no existe o es nulo, se ignora.
    if entity_id is None:
        continue

    # Se usa el método `match` de la expresión regular para comprobar el formato.
    # Si no hay coincidencia (el formato es incorrecto)...
    if not id_pattern.match(entity_id):
        # ...se añade un mensaje de error a la lista, incluyendo el número de línea y el valor incorrecto.
        invalid_ids.append(f"Line {i}: Invalid format for RP_ENTITY_ID: '{entity_id}'")

# Al igual que en el test anterior, si se encontraron errores, el test falla
# y muestra un reporte completo.
if invalid_ids:
    report = "\n".join(invalid_ids)
    pytest.fail(f"...\n{report}", pytrace=False)
```
