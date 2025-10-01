#!/usr/bin/env python3
import json
from collections import defaultdict, Counter
import re

def analyze_document_ids(input_file):
    """
    Analyzes specifically the RP_DOCUMENT_ID and their characteristics
    """
    
    document_info = defaultdict(lambda: {
        'title': None,
        'timestamp': None,
        'source': None,
        'entity_count': 0,
        'entities': [],
        'entity_types': set(),
        'word_count': None,
        'paragraph_count': None,
        'document_type': None,
        'language': None
    })
    
    id_patterns = {}
    total_records = 0
    
    print("Analyzing RP_DOCUMENT_ID...")
    
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    for record in data:
        doc_id = record.get('RP_DOCUMENT_ID')
        total_records += 1
        
        if doc_id:
            # Collect document information
            doc_info = document_info[doc_id]
            
            # Basic info (we take from the first record of the document)
            if doc_info['title'] is None:
                doc_info['title'] = record.get('TITLE')
                doc_info['timestamp'] = record.get('TIMESTAMP_UTC')
                doc_info['source'] = record.get('SOURCE_NAME')
                doc_info['word_count'] = record.get('WORD_COUNT')
                doc_info['paragraph_count'] = record.get('PARAGRAPH_COUNT')
                doc_info['document_type'] = record.get('DOCUMENT_TYPE')
                doc_info['language'] = record.get('ORIGINAL_LANGUAGE')
            
            # Document entities
            entity_name = record.get('ENTITY_NAME')
            entity_type = record.get('ENTITY_TYPE')
            
            if entity_name:
                doc_info['entities'].append({
                    'name': entity_name,
                    'type': entity_type,
                    'relevance': record.get('ENTITY_RELEVANCE'),
                    'sentiment': record.get('ENTITY_SENTIMENT')
                })
                doc_info['entity_types'].add(entity_type)
            
            doc_info['entity_count'] = record.get('DOCUMENT_RECORD_COUNT', 0)
            
            # Analyze ID format
            if doc_id not in id_patterns:
                id_patterns[doc_id] = {
                    'length': len(doc_id),
                    'chars': set(doc_id.upper()),
                    'is_hex': all(c in '0123456789ABCDEF' for c in doc_id.upper())
                }
    
    return dict(document_info), id_patterns, total_records

def create_document_id_report(document_info, id_patterns, total_records):
    """
    Crea un reporte detallado sobre RP_DOCUMENT_ID
    """
    
    report = []
    report.append("=== ANÁLISIS DETALLADO DE RP_DOCUMENT_ID ===\n")
    
    # Estadísticas generales
    unique_docs = len(document_info)
    avg_entities_per_doc = sum(info['entity_count'] for info in document_info.values()) / len(document_info) if document_info else 0
    
    report.append(f"Total de registros analizados: {total_records:,}")
    report.append(f"Documentos únicos: {unique_docs:,}")
    report.append(f"Promedio de entidades por documento: {avg_entities_per_doc:.2f}\n")
    
    # Análisis del formato de ID
    report.append("=== ANÁLISIS DEL FORMATO DE ID ===")
    
    if id_patterns:
        lengths = [pattern['length'] for pattern in id_patterns.values()]
        length_counter = Counter(lengths)
        
        report.append("Longitudes de ID encontradas:")
        for length, count in sorted(length_counter.items()):
            report.append(f"  {length} caracteres: {count} documentos")
        
        # Verificar si son hexadecimales
        hex_count = sum(1 for pattern in id_patterns.values() if pattern['is_hex'])
        report.append(f"\nIDs hexadecimales: {hex_count}/{len(id_patterns)} ({hex_count/len(id_patterns)*100:.1f}%)")
        
        # Caracteres únicos en todos los IDs
        all_chars = set()
        for pattern in id_patterns.values():
            all_chars.update(pattern['chars'])
        
        report.append(f"Caracteres únicos en IDs: {len(all_chars)}")
        report.append(f"Caracteres: {sorted(all_chars)}")
    
    report.append("")
    
    # Top documentos por número de entidades
    report.append("=== DOCUMENTOS CON MÁS ENTIDADES (TOP 10) ===")
    sorted_docs = sorted(document_info.items(), 
                        key=lambda x: x[1]['entity_count'], 
                        reverse=True)
    
    for i, (doc_id, info) in enumerate(sorted_docs[:10], 1):
        report.append(f"{i:2d}. Entidades: {info['entity_count']:2d} | {info['title'][:60]}...")
        report.append(f"     ID: {doc_id}")
        report.append(f"     Fuente: {info['source']}")
        report.append(f"     Palabras: {info['word_count']}, Párrafos: {info['paragraph_count']}")
    
    report.append("")
    
    # Análisis de tipos de documentos
    report.append("=== TIPOS DE DOCUMENTOS ===")
    doc_types = Counter(info['document_type'] for info in document_info.values())
    for doc_type, count in doc_types.most_common():
        percentage = (count / len(document_info)) * 100
        report.append(f"{doc_type}: {count} documentos ({percentage:.1f}%)")
    
    report.append("")
    
    # Análisis de idiomas
    report.append("=== IDIOMAS DE DOCUMENTOS ===")
    languages = Counter(info['language'] for info in document_info.values())
    for lang, count in languages.most_common():
        percentage = (count / len(document_info)) * 100
        report.append(f"{lang}: {count} documentos ({percentage:.1f}%)")
    
    report.append("")
    
    # Análisis de fuentes
    report.append("=== PRINCIPALES FUENTES (TOP 10) ===")
    sources = Counter(info['source'] for info in document_info.values())
    for source, count in sources.most_common(10):
        percentage = (count / len(document_info)) * 100
        report.append(f"{source}: {count} documentos ({percentage:.1f}%)")
    
    report.append("")
    
    # Distribución de entidades por documento
    report.append("=== DISTRIBUCIÓN DE ENTIDADES POR DOCUMENTO ===")
    entity_counts = [info['entity_count'] for info in document_info.values()]
    entity_distribution = Counter(entity_counts)
    
    report.append("Número de entidades | Documentos")
    for count, docs in sorted(entity_distribution.items()):
        percentage = (docs / len(document_info)) * 100
        report.append(f"{count:15d} | {docs:3d} documentos ({percentage:.1f}%)")
    
    report.append("")
    
    # Ejemplos de documentos representativos
    report.append("=== EJEMPLOS DE DOCUMENTOS REPRESENTATIVOS ===")
    
    # Documento con más entidades
    max_entities_doc = max(document_info.items(), key=lambda x: x[1]['entity_count'])
    report.append("📊 DOCUMENTO CON MÁS ENTIDADES:")
    report.append(f"ID: {max_entities_doc[0]}")
    report.append(f"Título: {max_entities_doc[1]['title']}")
    report.append(f"Entidades: {max_entities_doc[1]['entity_count']}")
    report.append(f"Tipos de entidades: {', '.join(sorted(max_entities_doc[1]['entity_types']))}")
    
    report.append("")
    
    # Documento con menos entidades
    min_entities_doc = min(document_info.items(), key=lambda x: x[1]['entity_count'])
    report.append("📄 DOCUMENTO CON MENOS ENTIDADES:")
    report.append(f"ID: {min_entities_doc[0]}")
    report.append(f"Título: {min_entities_doc[1]['title']}")
    report.append(f"Entidades: {min_entities_doc[1]['entity_count']}")
    
    return "\n".join(report)

def main():
    input_file = "/Users/franciscocidruiz/Documents/Projects/pytest/rt-feed-record-formatted.json"
    output_file = "/Users/franciscocidruiz/Documents/Projects/pytest/document_id_analysis.txt"
    
    print("Iniciando análisis de RP_DOCUMENT_ID...")
    
    document_info, id_patterns, total_records = analyze_document_ids(input_file)
    
    report = create_document_id_report(document_info, id_patterns, total_records)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"Análisis completado. Reporte guardado en: {output_file}")
    
    # Resumen en consola
    print(f"\n📊 RESUMEN:")
    print(f"- Total registros: {total_records:,}")
    print(f"- Documentos únicos: {len(document_info):,}")
    print(f"- Promedio entidades/doc: {sum(info['entity_count'] for info in document_info.values()) / len(document_info):.2f}")
    
    if id_patterns:
        lengths = [pattern['length'] for pattern in id_patterns.values()]
        print(f"- Longitud típica ID: {Counter(lengths).most_common(1)[0][0]} caracteres")

if __name__ == "__main__":
    main()