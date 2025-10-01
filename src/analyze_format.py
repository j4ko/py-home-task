#!/usr/bin/env python3
import json
from collections import Counter, defaultdict
import re

def detailed_character_analysis(input_file):
    """
    Detailed character analysis in RP_ENTITY_ID
    """
    
    all_chars = []
    entity_ids = []
    hex_violations = []
    
    print("Analyzing characters in RP_ENTITY_ID...")
    
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    for record in data:
        entity_id = record.get('RP_ENTITY_ID')
        if entity_id:
            entity_ids.append(entity_id)
            all_chars.extend(list(entity_id.upper()))
            
            # Check if contains non-hexadecimal characters
            non_hex_chars = [c for c in entity_id.upper() if c not in '0123456789ABCDEF']
            if non_hex_chars:
                hex_violations.append({
                    'id': entity_id,
                    'name': record.get('ENTITY_NAME'),
                    'non_hex_chars': non_hex_chars
                })
    
    return all_chars, entity_ids, hex_violations

def analyze_encoding_possibilities(entity_ids):
    """
    Analyzes what encoding system is being used
    """
    
    char_frequency = Counter()
    position_analysis = defaultdict(Counter)
    
    for entity_id in entity_ids:
        # General character frequency
        for char in entity_id.upper():
            char_frequency[char] += 1
        
        # Analysis by position
        for pos, char in enumerate(entity_id.upper()):
            position_analysis[pos][char] += 1
    
    return char_frequency, position_analysis

def create_detailed_format_report(all_chars, entity_ids, hex_violations, char_frequency, position_analysis):
    """
    Creates a detailed report about the format
    """
    
    report = []
    report.append("=== DETAILED ANALYSIS OF RP_ENTITY_ID FORMAT ===\n")
    
    # Basic statistics
    unique_chars = set(all_chars)
    report.append(f"Total IDs analyzed: {len(entity_ids):,}")
    report.append(f"Unique characters found: {len(unique_chars)}")
    report.append(f"Characters: {sorted(unique_chars)}\n")
    
    # Format verification
    hex_chars = set('0123456789ABCDEF')
    is_pure_hex = unique_chars.issubset(hex_chars)
    
    report.append("=== FORMAT VERIFICATION ===")
    report.append(f"Is pure hexadecimal? {is_pure_hex}")
    report.append(f"Valid hexadecimal characters: {sorted(unique_chars.intersection(hex_chars))}")
    
    non_hex = unique_chars - hex_chars
    if non_hex:
        report.append(f"NON-hexadecimal characters: {sorted(non_hex)}")
        report.append(f"Number of extra characters: {len(non_hex)}")
    report.append("")
    
    # Ejemplos de violaciones hexadecimales
    if hex_violations:
        report.append("=== EJEMPLOS DE IDs NO-HEXADECIMALES ===")
        for i, violation in enumerate(hex_violations[:10], 1):
            report.append(f"{i:2d}. {violation['id']} -> {violation['name']}")
            report.append(f"    Caracteres problemáticos: {violation['non_hex_chars']}")
        
        if len(hex_violations) > 10:
            report.append(f"... y {len(hex_violations) - 10} más\n")
        else:
            report.append("")
    
    # Análisis de sistema de numeración
    report.append("=== SISTEMA DE NUMERACIÓN DETECTADO ===")
    total_unique = len(unique_chars)
    
    systems = {
        10: "Decimal (0-9)",
        16: "Hexadecimal (0-9, A-F)",
        26: "Alfabético (A-Z)",
        36: "Alfanumérico completo (0-9, A-Z)",
        62: "Base62 (0-9, A-Z, a-z)"
    }
    
    report.append(f"Caracteres únicos detectados: {total_unique}")
    if total_unique in systems:
        report.append(f"Sistema probable: {systems[total_unique]}")
    else:
        report.append(f"Sistema personalizado con {total_unique} caracteres")
    
    report.append("")
    
    # Distribución de caracteres
    report.append("=== DISTRIBUCIÓN DE CARACTERES ===")
    report.append("Los 10 caracteres más frecuentes:")
    for char, count in char_frequency.most_common(10):
        percentage = (count / sum(char_frequency.values())) * 100
        report.append(f"  {char}: {count:,} veces ({percentage:.2f}%)")
    
    report.append("")
    
    # Análisis por posición
    report.append("=== ANÁLISIS POR POSICIÓN ===")
    for pos in range(6):  # Asumiendo IDs de 6 caracteres
        if pos in position_analysis:
            unique_at_pos = len(position_analysis[pos])
            most_common = position_analysis[pos].most_common(3)
            report.append(f"Posición {pos + 1}: {unique_at_pos} caracteres únicos")
            report.append(f"  Más comunes: {', '.join([f'{char}({count})' for char, count in most_common])}")
    
    report.append("")
    
    # Patrones detectados
    report.append("=== PATRONES DETECTADOS ===")
    
    # Verificar si hay patrones secuenciales
    sequential_count = 0
    for entity_id in entity_ids[:100]:  # Revisar primeros 100
        if is_sequential(entity_id):
            sequential_count += 1
    
    report.append(f"IDs con patrones secuenciales (en muestra de 100): {sequential_count}")
    
    # Verificar si empiezan con ciertos patrones
    starts_with_patterns = Counter(eid[0] for eid in entity_ids)
    report.append("Primeros caracteres más comunes:")
    for char, count in starts_with_patterns.most_common(10):
        percentage = (count / len(entity_ids)) * 100
        report.append(f"  {char}: {count:,} IDs ({percentage:.2f}%)")
    
    return "\n".join(report)

def is_sequential(entity_id):
    """
    Verifica si un ID tiene patrones secuenciales obvios
    """
    # Patrones como 123456, ABCDEF, etc.
    for i in range(len(entity_id) - 2):
        if entity_id[i:i+3] in ['123', '234', '345', '456', '567', '678', '789', 
                               'ABC', 'BCD', 'CDE', 'DEF', 'EFG', 'FGH']:
            return True
    return False

def main():
    input_file = "/Users/franciscocidruiz/Documents/Projects/pytest/rt-feed-record-formatted.json"
    output_file = "/Users/franciscocidruiz/Documents/Projects/pytest/entity_id_format_analysis.txt"
    
    print("Iniciando análisis detallado de formato...")
    
    all_chars, entity_ids, hex_violations = detailed_character_analysis(input_file)
    char_frequency, position_analysis = analyze_encoding_possibilities(entity_ids)
    
    report = create_detailed_format_report(
        all_chars, entity_ids, hex_violations, 
        char_frequency, position_analysis
    )
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"Análisis completado. Reporte guardado en: {output_file}")
    
    # Resumen en consola
    unique_chars = set(all_chars)
    hex_chars = set('0123456789ABCDEF')
    is_pure_hex = unique_chars.issubset(hex_chars)
    
    print(f"\n🔍 RESUMEN:")
    print(f"- Total IDs: {len(entity_ids):,}")
    print(f"- Caracteres únicos: {len(unique_chars)}")
    print(f"- ¿Hexadecimal puro? {is_pure_hex}")
    print(f"- Violaciones hex: {len(hex_violations):,}")
    
    if not is_pure_hex:
        non_hex = unique_chars - hex_chars
        print(f"- Caracteres extra: {sorted(non_hex)}")

if __name__ == "__main__":
    main()