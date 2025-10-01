
import json
from pathlib import Path

# --- Razonamiento de la Implementación ---
# 1. Ubicación del Fichero: Usamos `pathlib.Path` para construir la ruta al fichero de datos
#    de una manera robusta y compatible con diferentes sistemas operativos.
#    La ruta se construye relativamente al fichero de test actual.
#
# 2. Estructura del Test: La función `test_count_unique_documents` sigue la convención de
#    `pytest`. Todo el código de validación se encuentra dentro de esta función.
#
# 3. Lectura Eficiente: El fichero se abre con `with open(...)` y se itera línea por línea.
#    Esto es eficiente en uso de memoria, ya que no se lee el fichero completo de una vez.
#
# 4. Conteo de Únicos con un Set: Se utiliza un `set` llamado `unique_document_ids`.
#    Los sets en Python tienen la propiedad de que solo almacenan valores únicos.
#    Al añadir cada `RP_DOCUMENT_ID` al set, los duplicados se descartan automáticamente.
#    Esta es la forma más "Pythónica" y eficiente de contar elementos únicos.
#
# 5. Parseo y Robustez: Cada línea se parsea con `json.loads()`. Se incluye un bloque
#    `try...except json.JSONDecodeError` para manejar posibles líneas malformadas o vacías
#    en el fichero, lo que hace el script más robusto.
#
# 6. Verificación y Reporte: Al final, `len(unique_document_ids)` nos da el conteo exacto.
#    Usamos `print()` para mostrar el resultado de forma clara en la consola.
#    La aserción `assert total_unique_documents > 0` sirve como una comprobación
#    básica para asegurar que el fichero fue leído y procesado correctamente.

def test_count_unique_documents():
    """
    Verifica el número total de documentos únicos en el fichero de entrada.
    """
    # Construir la ruta al fichero de datos de forma relativa
    data_file_path = Path(__file__).parent / "data" / "rt-feed-record"

    unique_document_ids = set()

    try:
        with data_file_path.open('r', encoding='utf-8') as f:
            for line in f:
                # Ignorar líneas en blanco
                if not line.strip():
                    continue
                try:
                    data = json.loads(line)
                    # Añadir el ID del documento al set. Los duplicados serán ignorados.
                    if 'RP_DOCUMENT_ID' in data:
                        unique_document_ids.add(data['RP_DOCUMENT_ID'])
                except json.JSONDecodeError:
                    print(f"Aviso: No se pudo decodificar una línea JSON: {line.strip()}")

    except FileNotFoundError:
        assert False, f"El fichero de datos no se encontró en la ruta: {data_file_path}"

    # El número total de documentos únicos es el tamaño del set
    total_unique_documents = len(unique_document_ids)

    # Imprimimos el resultado para la verificación manual
    print(f"\nEl número total de documentos únicos encontrados es: {total_unique_documents}")

    # Aserción del test: verificamos que se haya encontrado al menos un documento
    assert total_unique_documents > 0
